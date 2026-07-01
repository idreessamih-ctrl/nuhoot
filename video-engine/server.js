/**
 * FFmux — RESTful FFmpeg Abstraction Microservice
 * 
 * Zero-marginal-cost video generation for autonomous AI agents.
 * Accepts JSON timeline → renders MP4 via FFmpeg.
 * 
 * Architecture (from research):
 * - POST /render → accepts JSON → returns { jobId }
 * - GET /status/:jobId → returns { status, progress, output_url }
 * - GET /outputs/:filename → downloads rendered file
 * 
 * Timeline JSON schema:
 * {
 *   "width": 1080,
 *   "height": 1920,        // 9:16 vertical for Reels
 *   "duration": 15,          // seconds
 *   "background": "#1A1A2E",
 *   "layers": [
 *     { "type": "image", "src": "/path/to/photo.jpg", "x": 0, "y": 0, "w": 1080, "h": 1080, "fit": "cover" },
 *     { "type": "text", "text": "العنوان", "x": 50, "y": 1100, "fontSize": 64, "color": "#FFFFFF", "font": "NotoKufiArabic" },
 *     { "type": "text", "text": "الوصف", "x": 50, "y": 1200, "fontSize": 32, "color": "#CCCCCC", "font": "NotoSansArabic" },
 *     { "type": "shape", "shape": "circle", "x": 900, "y": 100, "size": 80, "color": "#FF6B35", "opacity": 0.8 }
 *   ],
 *   "audio": { "src": "/path/to/music.mp3", "volume": 0.3 },
 *   "output": { "format": "mp4", "fps": 30, "quality": "high" }
 * }
 */

const express = require('express');
const ffmpeg = require('fluent-ffmpeg');
const ffmpegPath = require('ffmpeg-static');
const { v4: uuidv4 } = require('uuid');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configure FFmpeg path
ffmpeg.setFfmpegPath(ffmpegPath);

const app = express();
app.use(express.json({ limit: '50mb' }));
app.use(cors());

const PORT = process.env.FFMUX_PORT || 3100;
const OUTPUT_DIR = process.env.FFMUX_OUTPUT || '/tmp/ffmux-outputs';
const FONT_DIR = path.join(__dirname, 'fonts');
const TEMP_DIR = '/tmp/ffmux-temp';

fs.mkdirSync(OUTPUT_DIR, { recursive: true });
fs.mkdirSync(TEMP_DIR, { recursive: true });

// ─── Job Store (in-memory; use Redis for production) ───────
const jobs = new Map();

// ─── Font paths ────────────────────────────────────────────
const FONTS = {
  'NotoKufiArabic': path.join(FONT_DIR, 'NotoKufiArabic-Bold.ttf'),
  'NotoKufiArabic-Black': path.join(FONT_DIR, 'NotoKufiArabic-Black.ttf'),
  'NotoSansArabic': path.join(FONT_DIR, 'NotoSansArabic-Bold.ttf'),
  'Lato': path.join(FONT_DIR, 'Lato-Bold.ttf'),
  'DejaVuSans': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
};

function getFontPath(name) {
  return FONTS[name] || FONTS['NotoSansArabic'];
}

// ─── Escaping for FFmpeg drawtext ──────────────────────────
function escapeDrawText(text) {
  return text
    .replace(/\\/g, '\\\\')
    .replace(/:/g, '\\:')
    .replace(/'/g, "\\'")
    .replace(/%/g, '\\%')
    .replace(/,/g, '\\,');
}

// ─── Build FFmpeg filter complex from JSON timeline ────────
function buildFilterComplex(timeline) {
  const { width, height, duration, background, layers, audio } = timeline;
  const filters = [];
  const inputs = [];
  let inputIndex = 0;

  // Background: create a color source
  filters.push(`[bg]color=c=${background || 'black'}:s=${width}x${height}:d=${duration}[base]`);

  // Process each layer
  let prevLabel = 'base';
  
  for (let i = 0; i < layers.length; i++) {
    const layer = layers[i];
    const layerLabel = `layer${i}`;
    
    if (layer.type === 'image') {
      // Input image
      inputs.push({ type: 'image', src: layer.src, index: inputIndex });
      
      // Scale and position
      const fit = layer.fit || 'cover';
      let scaleFilter;
      if (fit === 'cover') {
        scaleFilter = `scale=${layer.w}:${layer.h}:force_original_aspect_ratio=increase,crop=${layer.w}:${layer.h}`;
      } else if (fit === 'contain') {
        scaleFilter = `scale=${layer.w}:${layer.h}:force_original_aspect_ratio=decrease,pad=${layer.w}:${layer.h}:(ow-iw)/2:(oh-ih)/2:color=black`;
      } else {
        scaleFilter = `scale=${layer.w}:${layer.h}`;
      }
      
      const opacity = layer.opacity !== undefined ? layer.opacity : 1;
      filters.push(`[${inputIndex}]${scaleFilter},setpts=PTS-STARTPTS[${layerLabel}_scaled]`);
      filters.push(`[${prevLabel}][${layerLabel}_scaled]overlay=${layer.x}:${layer.y}[${layerLabel}]`);
      inputIndex++;
      prevLabel = layerLabel;
      
    } else if (layer.type === 'text') {
      // Text overlay using drawtext
      const fontPath = getFontPath(layer.font || 'NotoSansArabic');
      const fontSize = layer.fontSize || 32;
      const color = (layer.color || '#FFFFFF').replace('#', '0x');
      const x = layer.x || 0;
      const y = layer.y || 0;
      const escapedText = escapeDrawText(layer.text);
      
      const drawtext = `drawtext=fontfile='${fontPath}':text='${escapedText}':fontcolor=${color}:fontsize=${fontSize}:x=${x}:y=${y}`;
      filters.push(`[${prevLabel}]${drawtext}[${layerLabel}]`);
      prevLabel = layerLabel;
      
    } else if (layer.type === 'shape') {
      // Shape overlay (circle, rectangle)
      if (layer.shape === 'circle') {
        // Create a circle using geq filter
        const size = layer.size || 50;
        const cx = size / 2;
        const cy = size / 2;
        const r = size / 2;
        const color = (layer.color || '#FF6B35').replace('#', '');
        const r_dec = parseInt(color.substring(0, 2), 16);
        const g_dec = parseInt(color.substring(2, 4), 16);
        const b_dec = parseInt(color.substring(4, 6), 16);
        const opacity = layer.opacity !== undefined ? layer.opacity : 1;
        
        filters.push(`[${prevLabel}]drawbox=x=${layer.x}:y=${layer.y}:w=${size}:h=${size}:color=${color}@${opacity}:t=fill[${layerLabel}]`);
        prevLabel = layerLabel;
      } else if (layer.shape === 'rectangle') {
        const w = layer.w || 100;
        const h = layer.h || 50;
        const color = (layer.color || '#FF6B35').replace('#', '');
        const opacity = layer.opacity !== undefined ? layer.opacity : 1;
        
        filters.push(`[${prevLabel}]drawbox=x=${layer.x}:y=${layer.y}:w=${w}:h=${h}:color=${color}@${opacity}:t=fill[${layerLabel}]`);
        prevLabel = layerLabel;
      }
    }
  }

  // Final output label
  const lastLabel = prevLabel === 'base' ? 'base' : prevLabel;
  
  return { filters, inputs, lastLabel };
}

// ─── Render video from timeline ────────────────────────────
function renderVideo(jobId, timeline) {
  const job = jobs.get(jobId);
  if (!job) return;

  try {
    const { width, height, duration, layers, audio } = timeline;
    const outputFile = path.join(OUTPUT_DIR, `${jobId}.mp4`);
    
    const { filters, inputs, lastLabel } = buildFilterComplex(timeline);
    const filterComplex = filters.join(';');
    
    // Build FFmpeg command
    const cmd = ffmpeg();
    
    // Add background color input
    cmd.input(`color=c=${timeline.background || 'black'}:s=${width}x${height}:d=${duration}:r=30`)
       .inputFormat('lavfi');
    
    // Add image inputs
    for (const input of inputs) {
      if (input.type === 'image') {
        cmd.input(input.src);
      }
    }
    
    // Add audio if specified
    if (audio && audio.src) {
      cmd.input(audio.src);
    }
    
    // Set filter complex
    cmd.complexFilter(filterComplex, lastLabel);
    
    // Output settings
    const fps = timeline.output?.fps || 30;
    const quality = timeline.output?.quality || 'high';
    const crf = quality === 'high' ? 18 : quality === 'medium' ? 23 : 28;
    
    cmd.outputOptions([
      `-c:v libx264`,
      `-preset medium`,
      `-crf ${crf}`,
      `-pix_fmt yuv420p`,
      `-r ${fps}`,
      `-t ${duration}`,
    ]);
    
    if (audio && audio.src) {
      cmd.outputOptions([
        `-c:a aac`,
        `-b:a 128k`,
        `-shortest`,
      ]);
      cmd.audioCodec('aac');
    }
    
    cmd.output(outputFile);
    
    // Track progress
    cmd.on('progress', (progress) => {
      if (jobs.has(jobId)) {
        jobs.get(jobId).progress = Math.round(progress.percent || 0);
      }
    });
    
    cmd.on('end', () => {
      const job = jobs.get(jobId);
      if (job) {
        job.status = 'finished';
        job.progress = 100;
        job.outputUrl = `/outputs/${jobId}.mp4`;
        job.fileSize = fs.statSync(outputFile).size;
        job.finishedAt = new Date();
        console.log(`✅ Job ${jobId} finished: ${outputFile} (${Math.round(job.fileSize / 1024 / 1024)}MB)`);
      }
    });
    
    cmd.on('error', (err) => {
      const job = jobs.get(jobId);
      if (job) {
        job.status = 'failed';
        job.error = err.message;
        job.finishedAt = new Date();
        console.error(`❌ Job ${jobId} failed: ${err.message}`);
      }
    });
    
    job.status = 'processing';
    job.startedAt = new Date();
    cmd.run();
    console.log(`▶️ Job ${jobId} started: ${layers?.length || 0} layers, ${duration}s, ${width}x${height}`);
    
  } catch (err) {
    job.status = 'failed';
    job.error = err.message;
    job.finishedAt = new Date();
    console.error(`❌ Job ${jobId} setup failed: ${err.message}`);
  }
}

// ─── Routes ────────────────────────────────────────────────

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', ffmpeg: ffmpegPath, version: '1.0.0' });
});

// POST /render — submit a render job
app.post('/render', (req, res) => {
  const timeline = req.body;
  
  // Validate required fields
  if (!timeline.width || !timeline.height || !timeline.duration) {
    return res.status(400).json({
      error: 'Missing required fields: width, height, duration'
    });
  }
  
  const jobId = uuidv4().substring(0, 8);
  jobs.set(jobId, {
    id: jobId,
    status: 'queued',
    progress: 0,
    timeline: { width: timeline.width, height: timeline.height, duration: timeline.duration },
    createdAt: new Date(),
  });
  
  // Start rendering (async)
  renderVideo(jobId, timeline);
  
  res.json({
    status: 'processing',
    jobId,
    message: `Render started. Poll /status/${jobId} for progress.`
  });
});

// GET /status/:jobId — check render status
app.get('/status/:jobId', (req, res) => {
  const job = jobs.get(req.params.jobId);
  if (!job) {
    return res.status(404).json({ error: 'Job not found' });
  }
  
  res.json({
    jobId: job.id,
    status: job.status,
    progress: job.progress,
    outputUrl: job.outputUrl || null,
    fileSize: job.fileSize || null,
    error: job.error || null,
    createdAt: job.createdAt,
    finishedAt: job.finishedAt || null,
  });
});

// GET /outputs/:filename — download rendered file
app.get('/outputs/:filename', (req, res) => {
  const filePath = path.join(OUTPUT_DIR, req.params.filename);
  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: 'File not found' });
  }
  res.sendFile(filePath);
});

// GET /jobs — list all jobs
app.get('/jobs', (req, res) => {
  const jobList = Array.from(jobs.values()).map(j => ({
    id: j.id,
    status: j.status,
    progress: j.progress,
    createdAt: j.createdAt,
  }));
  res.json({ jobs: jobList, total: jobList.length });
});

// ─── Start server ──────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`\n╔══════════════════════════════════════════╗`);
  console.log(`║  FFmux — Video Rendering Microservice    ║`);
  console.log(`║  Zero-marginal-cost FFmpeg REST API       ║`);
  console.log(`╠══════════════════════════════════════════╣`);
  console.log(`║  Port:     ${PORT}                          ║`);
  console.log(`║  FFmpeg:   ${ffmpegPath.substring(0, 20)}... ║`);
  console.log(`║  Output:   ${OUTPUT_DIR}     ║`);
  console.log(`║  Endpoints:                               ║`);
  console.log(`║    POST /render     → JSON → {jobId}      ║`);
  console.log(`║    GET  /status/:id → {status, progress}  ║`);
  console.log(`║    GET  /outputs/:f → download MP4        ║`);
  console.log(`║    GET  /health     → service check       ║`);
  console.log(`╚══════════════════════════════════════════╝\n`);
});

module.exports = app;
