// Generic render-check helper for this skill.
// Usage: NODE_PATH=/opt/node-tools/node_modules node screenshot.js <url-or-file-path> <output-prefix>
// Produces <prefix>-wide.png (1300x1400ish, full page) and <prefix>-mobile.png (420x900, full page).
// For local files, pass an absolute path starting with file:// or a plain path (will be resolved).
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const path = require('path');

const target = process.argv[2];
const prefix = process.argv[3] || 'shot';

function resolveTarget(t) {
  if (t.startsWith('http://') || t.startsWith('https://') || t.startsWith('file://')) return t;
  return 'file://' + path.resolve(t);
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await browser.newPage();
  const url = resolveTarget(target);

  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await page.setViewportSize({ width: 1300, height: 1400 });
  await page.waitForTimeout(600);
  await page.screenshot({ path: `${prefix}-wide.png`, fullPage: true });

  await page.setViewportSize({ width: 420, height: 900 });
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${prefix}-mobile.png`, fullPage: true });

  await browser.close();
  console.log(`wrote ${prefix}-wide.png and ${prefix}-mobile.png`);
})();
