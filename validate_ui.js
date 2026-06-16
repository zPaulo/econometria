const puppeteer = require('puppeteer');
const fs = require('fs');

if (!fs.existsSync('screenshots')) {
  fs.mkdirSync('screenshots');
}

const urls = [
  { name: 'home', url: 'http://localhost:3000' },
  { name: 'dashboard_tema1', url: 'http://localhost:3000/tema/1' },
  { name: 'aula_tema1', url: 'http://localhost:3000/tema/1/aula' },
  { name: 'teste_tema1', url: 'http://localhost:3000/tema/1/teste' },
];

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 1024 });

  for (const { name, url } of urls) {
    try {
      console.log(`Taking screenshot of ${url}`);
      await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      await page.screenshot({ path: `screenshots/${name}.png`, fullPage: true });
      console.log(`Saved screenshot to screenshots/${name}.png`);
    } catch (e) {
      console.error(`Failed on ${url}`, e);
    }
  }

  await browser.close();
  console.log('Validations generated.');
})();
