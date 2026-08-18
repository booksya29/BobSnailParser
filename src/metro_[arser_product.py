from patchright.async_api import async_playwright, Page, TimeoutError
import asyncio
from json_manager import read_json
from excel_add import add_to_excel

async def metro_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load {page.url}')
        return
    await page.wait_for_selector('div[class="titleDisplay"]')
    product_name = await page.locator('div[class="titleDisplay"]').locator('h2').text_content(timeout=2000)
    price_container = page.locator('div[class*="price-container"]')
    await page.wait_for_selector('div[class*="price-container"]')
    try:
        sale_price = await price_container.locator('span[class*="price-breakdown primary promotion"]').text_content(timeout=2000)
        price = await price_container.locator('span[class*="price-breakdown strike"]').text_content(timeout=2000)
    except TimeoutError:
        sale_price = '-'
        price = await price_container.locator('span[class*="price-breakdown primary"]').text_content(timeout=2000)
    try:
        producer = await page.locator('div[class="mfcss_article-detail--overview"]').locator('p', has_text='Бренд').locator('span').nth(1).text_content(timeout=2000)
    except TimeoutError:
        producer = '-'
    data = {'shop':'Метро','name':product_name.strip(), 'price':price.replace('\xa0грн  з ПДВ', '').replace('\xa0грн з ПДВ', '').strip(), 'sale_price':sale_price.replace('\xa0грн  з ПДВ', '').strip(), 'producer':producer.strip(), 'url':page.url}
    print(data)
    await add_to_excel(data)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await metro_parsing_one(page, 'https://shop.metro.ua/shop/pv/BTY-X342441/0032/0021/Bob-Snail-%D0%9D%D0%B0%D0%B1%D1%96%D1%80-%D0%A6%D1%83%D0%BA%D0%B5%D1%80%D0%BA%D0%B8-%D1%84%D1%80%D1%83%D0%BA%D1%82-%D0%AF%D0%B1%D0%BB%D1%83%D0%BA%D0%BE-%D0%B3%D1%80%D1%83%D1%88%D0%B0-20%D0%B3+%D1%96%D0%B3%D1%80%D0%B0%D1%88%D0%BA%D0%B0-1%D1%88%D1%82')

asyncio.run(test())