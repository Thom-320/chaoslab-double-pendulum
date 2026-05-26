const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const wait = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  const outDir = path.resolve(__dirname, '..', 'figures', 'slides_audit');
  fs.mkdirSync(outDir, { recursive: true });

  const htmlPath = 'file://' + path.resolve(__dirname, '..', 'presentation', 'index.html');
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(htmlPath, { waitUntil: 'networkidle0', timeout: 15000 });

  await wait(2500);

  const slideCount = await page.evaluate(() => document.querySelectorAll('.slide').length);
  console.log(`Found ${slideCount} slides`);

  for (let i = 0; i < slideCount; i++) {
    await page.evaluate((idx) => {
      if (typeof showSlide === 'function') showSlide(idx);
    }, i);
    await wait(3500);

    const sceneName = await page.evaluate((idx) => {
      return document.querySelectorAll('.slide')[idx]?.dataset?.scene || `slide_${idx}`;
    }, i);

    const filename = `slide_${String(i + 1).padStart(2, '0')}_${sceneName}.png`;
    await page.screenshot({ path: path.join(outDir, filename), type: 'png' });
    console.log(`✅ ${filename}`);
  }

  await browser.close();
  console.log(`\nAll ${slideCount} screenshots saved to ${outDir}`);
})();
