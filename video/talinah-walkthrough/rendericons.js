const { chromium } = require('playwright');
const fs = require('fs');
const dir = process.argv[2], out = process.argv[3];
const names = ['user-round', 'calendar-check', 'file-text', 'circle-check', 'message-square-text', 'sparkles',
  'search', 'briefcase-business', 'star', 'users-round', 'clipboard-check', 'send'];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 256, height: 256 } });
  for (const n of names) {
    let svg = fs.readFileSync(`${dir}/${n}.svg`, 'utf8').replace(/<!--.*?-->/s, '')
      .replace('width="24"', 'width="256"').replace('height="24"', 'height="256"')
      .replace('stroke="currentColor"', 'stroke="#2E9E55"').replace('stroke-width="2"', 'stroke-width="1.75"');
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await p.locator('svg').screenshot({ path: `${out}/${n}.png`, omitBackground: true });
  }
  await b.close();
})();
