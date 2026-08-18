from patchright.async_api import async_playwright, TimeoutError,  Page
import asyncio
from excel_add import add_to_excel
from json_manager import read_json
async def fozzy_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load {page.url}')
        return
    product_name = (await page.locator('div[class="product_name"]').text_content(timeout=3000)).strip()
    try:
        old_price = (await page.locator('div[class*="price_container"]').locator('span[class="old_price"]').first.text_content(timeout=3000)).strip()
    except TimeoutError:
        old_price = '-'
    regular_price = (await page.locator('div[class*="price_container"]').locator('span[class="regular_price"]').first.text_content(timeout=3000)).strip()
    if old_price == '-':
        price = regular_price
        sale_price = old_price
    else:
        price = old_price
        sale_price = regular_price
    producer = await page.locator('div[class="product_characteristics_item"]', has_text='Бренд').locator('a').text_content()

    data = {'shop':'Фоззі','name':product_name, 'price':price, 'sale_price':sale_price, 'producer':producer.strip(), 'url':page.url}
    print(data)
    await add_to_excel(data)

async def fozzy_parsing_all(page:Page):
    data = await read_json('fozzy.json')
    for item in data:
        await fozzy_parsing_one(page,item)

async def test():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=False)
        page = await b.new_page()
        await fozzy_parsing_one(page, "https://fozzyshop.ua/skhidni-solodoshchi-khalva/950652-pastyla-fruktova-premiia-grusha-iabluko-ta-iabluko-persyk.html")
asyncio.run(test())