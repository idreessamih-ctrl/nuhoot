#!/bin/bash
# Remotion batch render v2 — all 21 niches as PNG (with fixed captions + design)
cd /opt/nuhoot/remotion
OUTDIR="/tmp/nuhoot-remotion-v2"
mkdir -p "$OUTDIR"

CHROMIUM="/snap/chromium/current/usr/lib/chromium-browser/chrome"
CAPTIONS="/opt/nuhoot/remotion/captions.json"

# Niche → composition ID mapping (underscores become hyphens)
declare -A NICHE_MAP=(
  [restaurants]=restaurants [cafes]=cafes [bakeries]=bakeries
  [salons]=salons [spas]=spas [barbershops]=barbershops [gyms]=gyms
  [clinics]=clinics [dentists]=dentists [pharmacies]=pharmacies
  [dermatology]=dermatology [fashion]=fashion [perfumes]=perfumes
  [law_firms]=law-firms [real_estate]=real-estate [auto_shops]=auto-shops
  [car_wash]=car-wash [cleaning]=cleaning [hvac_ac]=hvac-ac
  [event_halls]=event-halls [training_centers]=training-centers
)

echo "Rendering 21 niches with Remotion v2..."
rendered=0; errors=0
start_time=$(date +%s)

for niche in $(python3 -c "import json; print(' '.join(sorted(json.load(open('$CAPTIONS')).keys())))"); do
  comp_id="${NICHE_MAP[$niche]:-$niche}"
  photo="photos/${niche}.jpg"
  
  PROPS=$(python3 -c "
import json
caps = json.load(open('$CAPTIONS'))
cap = caps.get('$niche', {})
print(json.dumps({
    'niche': '$niche',
    'headline': cap.get('headline', ''),
    'name': cap.get('name', ''),
    'taglines': cap.get('taglines', []),
    'hashtags': cap.get('hashtags', []),
    'cta': cap.get('cta', 'زورونا'),
    'photoPath': '$photo'
}))
")

  OUTPUT="$OUTDIR/${niche}.png"
  
  npx remotion still src/index.ts "$comp_id" "$OUTPUT" \
    --props="$PROPS" \
    --browser-executable="$CHROMIUM" \
    --log=error \
    2>/dev/null
  
  if [ -f "$OUTPUT" ] && [ $(stat -c%s "$OUTPUT" 2>/dev/null || echo 0) -gt 1000 ]; then
    SIZE=$(( $(stat -c%s "$OUTPUT") / 1024 ))
    echo "  $niche: ${SIZE}KB"
    rendered=$((rendered + 1))
  else
    echo "  ERROR $niche (retry with verbose...)"
    # Retry with verbose to see the error
    npx remotion still src/index.ts "$comp_id" "$OUTPUT" \
      --props="$PROPS" \
      --browser-executable="$CHROMIUM" \
      --log=error 2>&1 | tail -5
    if [ -f "$OUTPUT" ] && [ $(stat -c%s "$OUTPUT" 2>/dev/null || echo 0) -gt 1000 ]; then
      SIZE=$(( $(stat -c%s "$OUTPUT") / 1024 ))
      echo "  $niche: ${SIZE}KB (retry OK)"
      rendered=$((rendered + 1))
    else
      errors=$((errors + 1))
    fi
  fi
done

end_time=$(date +%s)
elapsed=$((end_time - start_time))
echo ""
echo "Done: $rendered rendered, $errors errors in ${elapsed}s"
