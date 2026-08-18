import asyncio

from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

async def fora_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load {page.url}')
        return
    product_name = await page.locator('h1[class="title"]').text_content()
    price_container = page.locator('div[class*="product-price-container"]').first
    try:
        price = await price_container.locator('div[class="old-integer"]').text_content(timeout=3000)
        sale_price_grn = await price_container.locator('div[class="current-integer"]').text_content(timeout=2000)
        sale_price_kop = await price_container.locator('div[class="current-fraction"]').text_content(timeout=2000)
        sale_price = f"{sale_price_grn}.{sale_price_kop}"
    except TimeoutError:
        sale_price = '-'
        price_grn = await price_container.locator('div[class="current-integer"]').text_content(timeout=2000)
        price_kop = await price_container.locator('div[class="current-fraction"]').text_content(timeout=2000)
        price = f"{price_grn}.{price_kop}"
    try:
        producer = await page.locator('div[class="product-details-column trademark"]', has_text='Торгова марка').locator('div[class="product-details-value"]').text_content()
    except TimeoutError:
        producer = '-'
    data = {'shop':'Фора','name':product_name, 'price':price, 'sale_price':sale_price, 'producer':producer.strip(), 'url':page.url}
    add_to_excel(data)

async def fora_parsing_all(page:Page):
    data = await read_json('fora.json')
    for item in data:
        fora_parsing_one(page, item)
        asyncio.sleep(1)