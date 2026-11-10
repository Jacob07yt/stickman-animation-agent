// Render an HTML page to an image (e.g. a thumbnail). Usage: node src/render/screenshot.cjs <page.html> <out.jpg> [width=1280] [height=720]
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [html, out, w, h] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(w || 1280), height: +(h || 720) } });
  await p.goto('file://' + path.resolve(html)); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: out, type: out.endsWith('.png') ? 'png' : 'jpeg', ...(out.endsWith('.png') ? {} : { quality: 92 }) });
  await b.close(); console.log(out);
})().catch(e => { console.error(e); process.exit(1); });
