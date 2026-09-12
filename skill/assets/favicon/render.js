const { chromium } = require('/opt/node-tools/node_modules/playwright');
const fs = require('fs');
const path = require('path');

const jobs = [
  { svg: 'icon.svg', size: 512, out: 'favicon-512.png' },
  { svg: 'icon.svg', size: 192, out: 'favicon-192.png' },
  { svg: 'icon.svg', size: 32, out: 'favicon-32.png' },
  { svg: 'icon.svg', size: 16, out: 'favicon-16.png' },
  { svg: 'icon.svg', size: 48, out: 'favicon-48.png' },
  { svg: 'icon-square.svg', size: 180, out: 'apple-touch-icon.png' },
];

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  for (const job of jobs) {
    const svgContent = fs.readFileSync(path.join(__dirname, job.svg), 'utf8');
    const html = `<!doctype html><html><head><style>
      html,body{margin:0;padding:0;background:transparent;}
      svg{display:block;width:${job.size}px;height:${job.size}px;}
    </style></head><body>${svgContent}</body></html>`;
    const page = await browser.newPage({ viewport: { width: job.size, height: job.size } });
    await page.setContent(html);
    await page.screenshot({ path: path.join(__dirname, job.out), omitBackground: true });
    await page.close();
    console.log('wrote', job.out);
  }
  await browser.close();
})();
