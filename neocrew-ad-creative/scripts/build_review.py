#!/usr/bin/env python3
"""
Builds a self-contained review/download HTML page from rendered ad PNGs.
Each card can be selected (checkbox) and downloaded individually or in bulk.
Images are embedded as full-resolution JPEGs (quality ~70) — large enough to
stay under Claude Artifacts' 16MB cap for a batch of ~50, small enough to
still be ad-ready on download. Do NOT embed each image twice (once for
display, once for download) — read img.src from the DOM for both; a prior
version of this pipeline did that and doubled the page from 14MB to 29MB.

Usage:
    python3 build_review.py variants.json rendered_png_dir/ out.html [--jpeg-quality 70]
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile


def to_jpeg_b64(png_path, quality):
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
             png_path, "--out", tmp_path],
            check=True, capture_output=True,
        )
        with open(tmp_path, "rb") as f:
            return base64.b64encode(f.read()).decode("ascii")
    finally:
        os.unlink(tmp_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("variants_json")
    ap.add_argument("png_dir")
    ap.add_argument("out_html")
    ap.add_argument("--jpeg-quality", type=int, default=70)
    ap.add_argument("--title", default="NeoCrew Ad Creative — Review & Download")
    args = ap.parse_args()

    with open(args.variants_json) as f:
        variants = json.load(f)

    cards = []
    total_bytes = 0
    for i, v in enumerate(variants):
        label = v.get("label") or f"ad-{i+1:02d}"
        png_path = os.path.join(args.png_dir, f"{label}.png")
        if not os.path.exists(png_path):
            print(f"WARNING: {png_path} not found, skipping", file=sys.stderr)
            continue
        b64 = to_jpeg_b64(png_path, args.jpeg_quality)
        total_bytes += len(b64)
        headline_plain = v["headline"].replace("<br>", " ")
        cards.append(f'''
    <div class="card" data-label="{label}">
      <div class="thumb-wrap">
        <img src="data:image/jpeg;base64,{b64}" alt="{headline_plain}" loading="lazy">
        <button class="check" aria-label="select"></button>
        <button class="dl-one" aria-label="download">&darr;</button>
      </div>
      <div class="body">
        <div class="idtag">{label}</div>
        <div class="headline">{headline_plain}</div>
        <div class="meta-row">{v["cta"]}</div>
      </div>
    </div>''')

    est_mb = total_bytes / 1024 / 1024
    print(f"embedded {len(cards)} images, ~{est_mb:.1f}MB base64", file=sys.stderr)
    if est_mb > 15:
        print("WARNING: over ~15MB — Claude Artifacts cap out at 16MB. "
              "Lower --jpeg-quality or split into multiple pages.", file=sys.stderr)

    page = f'''<meta charset="utf-8">
<title>{args.title}</title>
<style>
  :root {{
    --bg: #F3F5FA; --surface: #FFFFFF; --border: #E1E5F0; --ink: #10162A;
    --muted: #5A6478; --accent: #2F6FEB; --chip-bg: #EEF2FC;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #0B0F1A; --surface: #121826; --border: #232B3D; --ink: #EDF1FB; --muted: #8793AD; --accent: #5B8DFF; --chip-bg: #1A2136; }}
  }}
  :root[data-theme="dark"] {{ --bg: #0B0F1A; --surface: #121826; --border: #232B3D; --ink: #EDF1FB; --muted: #8793AD; --accent: #5B8DFF; --chip-bg: #1A2136; }}
  :root[data-theme="light"] {{ --bg: #F3F5FA; --surface: #FFFFFF; --border: #E1E5F0; --ink: #10162A; --muted: #5A6478; --accent: #2F6FEB; --chip-bg: #EEF2FC; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font-family:-apple-system,'Helvetica Neue',Arial,sans-serif; padding:44px 40px 120px; }}
  .wrap {{ max-width: 1520px; margin: 0 auto; }}
  .eyebrow {{ font-size:12px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--accent); }}
  h1 {{ font-size:30px; font-weight:800; letter-spacing:-0.5px; margin:10px 0 20px; text-wrap:balance; }}
  .toolbar {{ display:flex; align-items:center; gap:10px; margin-bottom:22px; flex-wrap:wrap; }}
  .toolbar button {{ background:var(--surface); border:1px solid var(--border); color:var(--ink); font-size:13px; font-weight:600; padding:9px 16px; border-radius:10px; cursor:pointer; }}
  .toolbar button:hover {{ border-color:var(--accent); }}
  .toolbar .count {{ font-size:13px; color:var(--muted); }}
  .grid {{ display:grid; grid-template-columns:repeat(6, 1fr); gap:18px; }}
  @media (max-width:1400px){{ .grid{{grid-template-columns:repeat(5,1fr);}} }}
  @media (max-width:1150px){{ .grid{{grid-template-columns:repeat(4,1fr);}} }}
  @media (max-width:850px){{ .grid{{grid-template-columns:repeat(3,1fr);}} }}
  @media (max-width:600px){{ .grid{{grid-template-columns:repeat(2,1fr);}} body{{padding:28px 18px 120px;}} }}
  .card {{ background:var(--surface); border:1px solid var(--border); border-radius:13px; overflow:hidden; display:flex; flex-direction:column; transition:transform .12s ease, box-shadow .12s ease, border-color .12s ease; }}
  .card:hover {{ transform:translateY(-2px); box-shadow:0 12px 26px rgba(20,30,60,0.14); }}
  .card.selected {{ border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent); }}
  .thumb-wrap {{ position:relative; cursor:zoom-in; }}
  .card img {{ width:100%; display:block; aspect-ratio:1080/1350; object-fit:cover; background:var(--chip-bg); }}
  .card .body {{ padding:10px 11px 12px; display:flex; flex-direction:column; gap:5px; }}
  .idtag {{ font-size:9.5px; font-weight:700; color:var(--accent); letter-spacing:0.4px; }}
  .headline {{ font-size:11.5px; font-weight:700; line-height:1.28; }}
  .meta-row {{ font-size:9.5px; color:var(--muted); }}
  .check {{
    position:absolute; top:8px; left:8px; width:26px; height:26px; border-radius:8px;
    background:rgba(10,14,24,0.55); border:1.5px solid rgba(255,255,255,0.6); cursor:pointer;
    backdrop-filter: blur(2px);
  }}
  .card.selected .check {{ background:var(--accent); border-color:var(--accent); }}
  .card.selected .check::after {{
    content:''; position:absolute; left:7px; top:3px; width:6px; height:12px;
    border:solid white; border-width:0 2px 2px 0; transform:rotate(45deg);
  }}
  .dl-one {{
    position:absolute; top:8px; right:8px; width:26px; height:26px; border-radius:8px;
    background:rgba(10,14,24,0.55); border:1.5px solid rgba(255,255,255,0.6); color:#fff;
    font-size:13px; font-weight:700; cursor:pointer; backdrop-filter: blur(2px);
  }}
  .dl-one:hover, .check:hover {{ background:var(--accent); border-color:var(--accent); }}
  .dlbar {{
    position:fixed; left:50%; bottom:22px; transform:translateX(-50%);
    background:var(--surface); border:1px solid var(--border); border-radius:14px;
    padding:10px 12px 10px 18px; display:flex; align-items:center; gap:12px;
    box-shadow:0 16px 40px rgba(10,15,30,0.25); z-index:8;
  }}
  .dlbar span {{ font-size:13px; font-weight:600; color:var(--ink); }}
  .dlbar button {{ background:var(--accent); color:#fff; border:none; font-size:13px; font-weight:700; padding:10px 18px; border-radius:9px; cursor:pointer; }}
  .dlbar button.secondary {{ background:transparent; color:var(--muted); font-weight:600; padding:10px 12px; }}
  .lightbox {{ position:fixed; inset:0; background:rgba(6,9,18,0.85); display:none; align-items:center; justify-content:center; padding:40px; z-index:20; cursor:zoom-out; }}
  .lightbox.open {{ display:flex; }}
  .lightbox img {{ max-height:100%; max-width:440px; border-radius:14px; box-shadow:0 30px 80px rgba(0,0,0,0.5); }}
</style>

<div class="wrap">
  <div class="eyebrow">NeoCrew &middot; Ad Creative</div>
  <h1>{args.title}</h1>

  <div class="toolbar">
    <button id="select-all">Select all</button>
    <button id="clear-sel">Clear</button>
    <span class="count" id="count">0 selected</span>
  </div>

  <div class="grid" id="grid">
    {"".join(cards)}
  </div>
</div>

<div class="lightbox" id="lightbox"><img id="lightbox-img" src=""></div>

<div class="dlbar" id="dlbar" style="display:none;">
  <span id="dlbar-count">0 selected</span>
  <button class="secondary" id="dlbar-clear">Clear</button>
  <button id="dlbar-download">Download selected</button>
</div>

<script>
  const cards = Array.from(document.querySelectorAll('.card'));
  const countEl = document.getElementById('count');
  const dlbar = document.getElementById('dlbar');
  const dlbarCount = document.getElementById('dlbar-count');
  const selected = new Set();

  const dlbarBtn = document.getElementById('dlbar-download');
  function refreshCounts() {{
    const n = selected.size;
    countEl.textContent = n + ' selected';
    dlbarCount.textContent = n + ' selected';
    dlbar.style.display = n > 0 ? 'flex' : 'none';
    dlbarBtn.textContent = n > 1 ? 'Download selected (.zip)' : 'Download selected';
  }}

  function toggleCard(card, force) {{
    const label = card.dataset.label;
    const shouldSelect = force !== undefined ? force : !selected.has(label);
    if (shouldSelect) {{ selected.add(label); card.classList.add('selected'); }}
    else {{ selected.delete(label); card.classList.remove('selected'); }}
    refreshCounts();
  }}

  function downloadOne(dataUrl, filename) {{
    const a = document.createElement('a');
    a.href = dataUrl;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  }}

  // Minimal ZIP writer (STORE method, no compression — the JPEGs inside are
  // already compressed, so there's nothing to gain from deflating them).
  // Bulk downloads bundle into ONE zip instead of firing N separate
  // download() calls: Chrome silently blocks automatic multi-file downloads
  // after the first one when they're not each tied to a fresh user gesture,
  // so triggering several downloads in a loop quietly drops all but the
  // first — a real bug caught by testing this exact flow, not a hypothetical.
  function crc32(bytes) {{
    if (!crc32.table) {{
      const t = [];
      for (let n = 0; n < 256; n++) {{
        let c = n;
        for (let k = 0; k < 8; k++) c = c & 1 ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        t[n] = c >>> 0;
      }}
      crc32.table = t;
    }}
    let crc = 0xFFFFFFFF;
    for (let i = 0; i < bytes.length; i++) crc = (crc >>> 8) ^ crc32.table[(crc ^ bytes[i]) & 0xFF];
    return (crc ^ 0xFFFFFFFF) >>> 0;
  }}

  function dataUrlToBytes(dataUrl) {{
    const bin = atob(dataUrl.split(',')[1]);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return bytes;
  }}

  function buildZip(files) {{
    const encoder = new TextEncoder();
    const localParts = [];
    const centralParts = [];
    let offset = 0;

    files.forEach(({{name, bytes}}) => {{
      const nameBytes = encoder.encode(name);
      const crc = crc32(bytes);
      const size = bytes.length;

      const lh = new Uint8Array(30 + nameBytes.length);
      const lv = new DataView(lh.buffer);
      lv.setUint32(0, 0x04034b50, true);
      lv.setUint16(4, 20, true);
      lv.setUint16(6, 0, true);
      lv.setUint16(8, 0, true);
      lv.setUint16(10, 0, true);
      lv.setUint16(12, 0x21, true);
      lv.setUint32(14, crc, true);
      lv.setUint32(18, size, true);
      lv.setUint32(22, size, true);
      lv.setUint16(26, nameBytes.length, true);
      lv.setUint16(28, 0, true);
      lh.set(nameBytes, 30);
      localParts.push(lh, bytes);

      const ch = new Uint8Array(46 + nameBytes.length);
      const cv = new DataView(ch.buffer);
      cv.setUint32(0, 0x02014b50, true);
      cv.setUint16(4, 20, true);
      cv.setUint16(6, 20, true);
      cv.setUint16(8, 0, true);
      cv.setUint16(10, 0, true);
      cv.setUint16(12, 0, true);
      cv.setUint16(14, 0x21, true);
      cv.setUint32(16, crc, true);
      cv.setUint32(20, size, true);
      cv.setUint32(24, size, true);
      cv.setUint16(28, nameBytes.length, true);
      cv.setUint32(42, offset, true);
      ch.set(nameBytes, 46);
      centralParts.push(ch);

      offset += lh.length + bytes.length;
    }});

    const centralSize = centralParts.reduce((a, p) => a + p.length, 0);
    const end = new Uint8Array(22);
    const ev = new DataView(end.buffer);
    ev.setUint32(0, 0x06054b50, true);
    ev.setUint16(8, files.length, true);
    ev.setUint16(10, files.length, true);
    ev.setUint32(12, centralSize, true);
    ev.setUint32(16, offset, true);

    return new Blob([...localParts, ...centralParts, end], {{type: 'application/zip'}});
  }}

  cards.forEach(card => {{
    const check = card.querySelector('.check');
    const dlOne = card.querySelector('.dl-one');
    const thumb = card.querySelector('.thumb-wrap');
    const imgSrc = card.querySelector('img').src;
    check.addEventListener('click', (e) => {{ e.stopPropagation(); toggleCard(card); }});
    dlOne.addEventListener('click', (e) => {{
      e.stopPropagation();
      downloadOne(imgSrc, card.dataset.label + '.jpg');
    }});
    thumb.addEventListener('click', () => {{
      document.getElementById('lightbox-img').src = imgSrc;
      document.getElementById('lightbox').classList.add('open');
    }});
  }});

  document.getElementById('lightbox').addEventListener('click', (e) => {{
    e.currentTarget.classList.remove('open');
  }});
  document.getElementById('select-all').addEventListener('click', () => cards.forEach(c => toggleCard(c, true)));
  document.getElementById('clear-sel').addEventListener('click', () => cards.forEach(c => toggleCard(c, false)));
  document.getElementById('dlbar-clear').addEventListener('click', () => cards.forEach(c => toggleCard(c, false)));

  document.getElementById('dlbar-download').addEventListener('click', () => {{
    const toDownload = cards.filter(c => selected.has(c.dataset.label));
    if (toDownload.length === 0) return;
    if (toDownload.length === 1) {{
      downloadOne(toDownload[0].querySelector('img').src, toDownload[0].dataset.label + '.jpg');
      return;
    }}
    const files = toDownload.map(card => ({{
      name: card.dataset.label + '.jpg',
      bytes: dataUrlToBytes(card.querySelector('img').src)
    }}));
    const blob = buildZip(files);
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'neocrew-ads-selected.zip';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 4000);
  }});

  refreshCounts();
</script>
'''

    with open(args.out_html, "w") as f:
        f.write(page)
    print(f"wrote {args.out_html} ({os.path.getsize(args.out_html) / 1024 / 1024:.1f}MB)")


if __name__ == "__main__":
    main()
