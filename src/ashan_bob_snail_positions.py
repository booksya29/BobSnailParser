from patchright.async_api import Page, async_playwright, TimeoutError
import asyncio
from json_manager import add_json



url = 'https://express.auchan.ua/search/Bob%20SNail/'



async def ashan_bob_snail_products(page:Page):
    global url
    urls_list = []
    await page.goto(url)
    while(True):
        try:
            await page.locator('div[class="page-item__button"]').locator('button').click(timeout=10000)
        except TimeoutError:
            await asyncio.sleep(2.5)
            break
    all_items_first = await page.locator('div[style="display:contents"]').all()
    all_items_second = await page.locator('div[style="display: contents;"]').all()
    all_items = all_items_first+all_items_second
    for item in all_items:
        url = await item.locator('a[class*="ProductCard_data__name"]').first.get_attribute('href')
        full_url = 'https://express.auchan.ua' + url
        urls_list.append(full_url)
    await add_json(urls_list, 'ashan.json')


async def test():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await ashan_bob_snail_products(page)




asyncio.run(test())