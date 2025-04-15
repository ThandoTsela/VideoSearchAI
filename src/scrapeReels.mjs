import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.instagram.com/reels/DGyHvbdOLxk/');

  // Extract data
  const data = await page.evaluate(() => {
    const titleElement = document.querySelector('span.xuxw1ft[dir="auto"]');
    const title = titleElement ? titleElement.innerText : null;
    const username = document.querySelector('a[href*="/reels/"]')?.innerText;
    const location = document.querySelector('a[href*="/explore/locations/"]')?.innerText;
    const hashtags = Array.from(document.querySelectorAll('a[href*="/tags/"]')).map(tag => tag.innerText);
    const thumbnail = document.querySelector('img')?.src;

    return {
      title,
      username,
      location,
      hashtags,
      thumbnail,
    };
  });

  console.log(data);

  await browser.close();
})();