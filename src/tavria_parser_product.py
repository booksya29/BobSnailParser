import asyncio

from patchright.async_api import async_playwright, Page, TimeoutError
from excel_add import add_to_excel
from json_manager import read_json

async def tavria_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load {page.url}')
        return
    product_name = await page.locator('h1[data-testid="detail-name"]').text_content()
    price_block = page.locator('div[class*="cart__actions__price"]').first
    try:
        price_unform = await price_block.locator('p[data-testid*="crossed-out-old"]').text_content(timeout=3000)
        sale_price = await price_block.locator('p[class*="base__price"]').text_content(timeout=3000)
    except:
        price_unform = await price_block.text_content(timeout=3000)
        sale_price = '-'
    price = price_unform.replace('Додати', '')
    sale_price.replace('Додати', '')
    producer = '-'
    data = {'shop':'Таврія','name':product_name, 'price':price, 'sale_price':sale_price, 'producer':producer.strip(), 'url':page.url}
    await add_to_excel(data)

async def tavria_parsing_all(page:Page):
    data = await read_json('tavria.json')
    for item in data:
        await tavria_parsing_one(page, item)
        await asyncio.sleep(1)