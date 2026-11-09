// Frame-accurate renderer for timeline compositions (window.__timelines + body data-duration).
// Seeks the GSAP timeline to each frame, screenshots it, and pipes JPEG frames into ffmpeg.
// Usage: node src/render/capture.cjs <scene.html> <out.mp4> [fps=30]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [html, out, fpsArg] = process.argv.slice(2);
  const fps = +(fpsArg || 30);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(html));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);
  const dur = +(await page.evaluate(() => document.body.dataset.duration));
  const frames = Math.round(dur * fps);
  const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(fps), out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < frames; i++) {
    await page.evaluate(t => { Object.values(window.__timelines)[0].seek(t, false); }, i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise((res, rej) => ff.on('close', c => (c === 0 ? res() : rej(new Error('ffmpeg exit ' + c)))));
  await browser.close();
  console.log(`${path.basename(out)} ${frames} frames ${dur}s`);
})().catch(e => { console.error(e); process.exit(1); });
