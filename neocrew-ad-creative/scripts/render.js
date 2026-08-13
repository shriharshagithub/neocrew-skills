#!/usr/bin/env node
/**
 * Renders generated ad HTML files to PNG via headless Chromium.
 *
 * Usage: node render.js <html_dir> <out_dir> [port]
 *
 * Requires a static file server rooted at the SKILL directory (so /assets/...
 * resolves) to already be running on the given port. Start one with:
 *   cd <skill_dir> && python3 -m http.server <port>
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const [, , htmlDirArg, outDirArg, portArg] = process.argv;
if (!htmlDirArg || !outDirArg) {
  console.error('usage: node render.js <html_dir> <out_dir> [port]');
  process.exit(1);
}

const SKILL_DIR = path.dirname(__dirname);
const HTML_DIR = path.resolve(htmlDirArg);
const OUT_DIR = path.resolve(outDirArg);
const PORT = portArg || '8934';

// html_dir must be reachable under the file server's document root (SKILL_DIR)
const REL = path.relative(SKILL_DIR, HTML_DIR);
if (REL.startsWith('..')) {
  console.error(`html_dir must be inside the skill directory (${SKILL_DIR}) so the local server can see it.`);
  process.exit(1);
}

async function main() {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });
  const files = fs.readdirSync(HTML_DIR).filter(f => f.endsWith('.html')).sort();

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });

  for (const file of files) {
    const id = file.replace('.html', '');
    const url = `http://localhost:${PORT}/${REL}/${file}`;
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.screenshot({ path: path.join(OUT_DIR, `${id}.png`) });
    console.log('rendered', id);
  }

  await browser.close();
  console.log(`done: ${files.length} images in ${OUT_DIR}`);
}

main().catch(err => { console.error(err); process.exit(1); });
