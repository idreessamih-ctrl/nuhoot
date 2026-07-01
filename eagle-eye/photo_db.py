#!/usr/bin/env python3
"""Nuhoot Photo Database — SQLite catalog + Openverse population + auto-tagging."""
import json, os, sqlite3, time
import cv2, numpy as np, httpx

DB_PATH = "/opt/nuhoot/photos/photos.db"
PHOTOS_DIR = "/opt/nuhoot/remotion/public/photos"

NICHES = ["restaurants","cafes","bakeries","salons","spas","barbershops","gyms",
    "clinics","dentists","pharmacies","dermatology","fashion","perfumes","law_firms",
    "real_estate","auto_shops","car_wash","cleaning","hvac_ac","event_halls",
    "training_centers"]

OPENVERSE_QUERIES = {
    "restaurants":"Saudi restaurant food kabsa","cafes":"Saudi Arabia coffee shop",
    "bakeries":"Arabic bakery bread dessert","salons":"beauty salon interior modern",
    "spas":"luxury spa wellness interior","barbershops":"barbershop interior modern",
    "gyms":"gym fitness equipment interior","clinics":"modern medical clinic interior",
    "dentists":"dental clinic modern","pharmacies":"pharmacy shelves medicine",
    "dermatology":"skincare clinic treatment","fashion":"Saudi fashion abaya boutique",
    "perfumes":"luxury perfume bottle oud","law_firms":"law office professional interior",
    "real_estate":"Saudi Riyadh modern villa","auto_shops":"auto mechanic garage workshop",
    "car_wash":"car wash detailing shine","cleaning":"clean service professional home",
    "hvac_ac":"air conditioner installation technician","event_halls":"Saudi wedding hall decoration",
    "training_centers":"classroom training education modern",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS photos (
    id TEXT PRIMARY KEY, path TEXT NOT NULL, niche TEXT NOT NULL, caption TEXT,
    tags TEXT, mood TEXT, has_human INTEGER DEFAULT 0, gender TEXT DEFAULT 'plural',
    width INTEGER, height INTEGER, dominant_colors TEXT, source TEXT, license TEXT,
    used_count INTEGER DEFAULT 0, last_used TEXT,
    created_at TEXT DEFAULT (datetime('now')));
CREATE TABLE IF NOT EXISTS composites (
    id TEXT PRIMARY KEY, niche TEXT NOT NULL, path TEXT NOT NULL, source_ids TEXT NOT NULL,
    technique TEXT, ad_id TEXT, created_at TEXT DEFAULT (datetime('now')));
CREATE INDEX IF NOT EXISTS idx_photos_niche ON photos(niche);
CREATE INDEX IF NOT EXISTS idx_photos_niche_human ON photos(niche, has_human);
"""

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn

def auto_tag(image_path):
    """Extract visual features from a photo using OpenCV."""
    img = cv2.imread(image_path)
    if img is None: return None
    h, w = img.shape[:2]
    mean_rgb = img.mean(axis=(0,1))[::-1]
    brightness = float(img.mean())
    aspect = w / h
    shot = "wide-angle" if aspect > 1.5 else ("portrait" if aspect < 0.8 else "standard")
    r, g, b = mean_rgb
    mood = "warm" if r > g > b else ("cool" if b > r else "neutral")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    skin = cv2.inRange(hsv, np.array([0,30,60]), np.array([25,170,255]))
    has_human = 1 if skin.sum() / (h*w*255) > 0.03 else 0
    return {"width":w,"height":h,"mood":"bright" if brightness>128 else "dark",
        "has_human":has_human,"tags":json.dumps([shot,mood]),
        "dominant_colors":json.dumps([f"#{int(mean_rgb[0]):02X}{int(mean_rgb[1]):02X}{int(mean_rgb[2]):02X}"])}

def tag_existing_photos():
    conn = get_db(); tagged = 0
    for niche in NICHES:
        fp = os.path.join(PHOTOS_DIR, f"{niche}.jpg")
        if not os.path.exists(fp): continue
        pid = f"{niche}_00"; tags = auto_tag(fp)
        if not tags: continue
        conn.execute("INSERT OR REPLACE INTO photos (id,path,niche,caption,tags,mood,"
            "has_human,width,height,dominant_colors,source,license) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid,f"photos/{niche}.jpg",niche,f"{niche} default photo",tags["tags"],
             tags["mood"],tags["has_human"],tags["width"],tags["height"],tags["dominant_colors"],
             "local","owned"))
        tagged += 1
    conn.commit(); conn.close()
    print(f"✓ Tagged {tagged} existing photos → {DB_PATH}")

def search_openverse(query, page_size=20):
    try:
        resp = httpx.get("https://api.openverse.org/v1/images/",
            params={"q":query,"license_type":"commercial","page_size":page_size}, timeout=30)
        resp.raise_for_status(); return resp.json().get("results",[])
    except Exception as e:
        print(f"  ⚠️ Openverse error for '{query}': {e}"); return []

def populate_from_openverse(max_per_niche=5):
    """Download up to N photos per niche from Openverse (no API key, 20 req/min)."""
    conn = get_db(); total = 0
    for niche in NICHES:
        query = OPENVERSE_QUERIES.get(niche, niche.replace("_"," "))
        results = search_openverse(query, page_size=max_per_niche+5); added = 0
        for r in results:
            if added >= max_per_niche: break
            url = r.get("url","")
            if not url.startswith("http"): continue
            pid = f"{niche}_{added+1:02d}"
            if conn.execute("SELECT id FROM photos WHERE id=?",(pid,)).fetchone(): continue
            fname = f"{niche}_{added+1:02d}.jpg"
            fp = os.path.join(PHOTOS_DIR, fname)
            try:
                data = httpx.get(url, timeout=60, follow_redirects=True).content
                with open(fp,"wb") as f: f.write(data)
            except Exception as e:
                print(f"  ⚠️ Download failed: {e}"); continue
            tags = auto_tag(fp)
            if not tags: continue
            conn.execute("INSERT OR REPLACE INTO photos (id,path,niche,caption,tags,mood,"
                "has_human,width,height,dominant_colors,source,license) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (pid,f"photos/{fname}",niche,r.get("title",""),tags["tags"],tags["mood"],
                 tags["has_human"],tags["width"],tags["height"],tags["dominant_colors"],
                 "openverse",r.get("license","cc-by")))
            added += 1; total += 1; time.sleep(3.5)
        conn.commit(); print(f"  {niche}: +{added} from Openverse")
    conn.close(); print(f"✓ Populated {total} photos from Openverse")

def photos_for_niche(niche, has_human=None, limit=10):
    conn = get_db(); q,p = "SELECT * FROM photos WHERE niche = ?",[niche]
    if has_human is not None: q += " AND has_human = ?"; p.append(int(has_human))
    q += " ORDER BY used_count ASC, RANDOM() LIMIT ?"; p.append(limit)
    rows = [dict(r) for r in conn.execute(q,p).fetchall()]; conn.close(); return rows

def get_photo_catalog_text(niche, limit=10):
    """Build PHOTO_CATALOG block for Kimi's prompt."""
    photos = photos_for_niche(niche, limit=limit)
    if not photos:
        return f'\nAVAILABLE PHOTOS for niche "{niche}": (none — use photos/{niche}.jpg)\n'
    lines = [f'\nAVAILABLE PHOTOS for niche "{niche}" (pick by id):']
    for ph in photos:
        tags = json.loads(ph.get("tags","[]"))
        human = "has human" if ph.get("has_human") else "no people"
        dims = f"{ph.get('width','?')}x{ph.get('height','?')}"
        lines.append(f'- {ph["id"]}: {ph.get("caption","photo")}, {", ".join(tags)}, {human}, {dims}')
    lines += ["RULES:","- PhotoSingle/PhotoArch/PhotoCircle → pick 1 id",
        "- PhotoGrid/PhotoMosaic/FrameStack → pick 2-3 ids (vary angles)",
        '- If ad mentions a person, prefer ids with "has human"',
        '- Use the id as the "src" value (e.g. "src": "restaurants_01")']
    return "\n".join(lines)+"\n"

def resolve_photo_id(photo_id, niche):
    """restaurants_03 → photos/restaurants_03.jpg (fallback to default)."""
    conn = get_db()
    row = conn.execute("SELECT path FROM photos WHERE id=? AND niche=?",(photo_id,niche)).fetchone()
    conn.close()
    if row: return row["path"]
    if photo_id.startswith("photos/") or photo_id.startswith("/"): return photo_id
    return f"photos/{niche}.jpg"

def mark_used(photo_id):
    conn = get_db()
    conn.execute("UPDATE photos SET used_count=used_count+1, last_used=datetime('now') WHERE id=?",(photo_id,))
    conn.commit(); conn.close()

def record_composite(cid, niche, path, source_ids, technique, ad_id):
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO composites (id,niche,path,source_ids,technique,ad_id) VALUES (?,?,?,?,?,?)",
        (cid,niche,path,json.dumps(source_ids),technique,ad_id))
    conn.commit(); conn.close()

if __name__ == "__main__":
    import sys; cmd = sys.argv[1] if len(sys.argv)>1 else "init"
    if cmd == "init": tag_existing_photos()
    elif cmd == "openverse": populate_from_openverse(int(sys.argv[2]) if len(sys.argv)>2 else 5)
    elif cmd == "stats":
        conn = get_db()
        for n in NICHES:
            print(f"  {n:20s}: {conn.execute('SELECT COUNT(*) FROM photos WHERE niche=?',(n,)).fetchone()[0]} photos")
        conn.close()
    else: print("Usage: python photo_db.py [init|openverse N|stats]")
