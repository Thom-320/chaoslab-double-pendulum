const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 2 });
  
  // Go to the presentation
  await page.goto('http://localhost:8000/presentation/index.html', { waitUntil: 'networkidle0' });
  
  if (!fs.existsSync('figures')) {
    fs.mkdirSync('figures');
  }

  const numSlides = await page.evaluate(() => document.querySelectorAll('.slide').length);
  
  for (let i = 0; i < numSlides; i++) {
    // Wait for animation to finish
    await new Promise(r => setTimeout(r, 1500));
    
    await page.screenshot({ path: `figures/slide_${i + 1}.png` });
    console.log(`Saved figures/slide_${i + 1}.png`);
    
    // Press ArrowRight to go to next slide
    await page.keyboard.press('ArrowRight');
  }

  await browser.close();
})();
