import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import add_json, read_json
from excel_add import add_to_excel
async def silpo_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load {page.url}')
        return
    product_name = await page.locator('h1[data-autotestid="product-page__title"]').text_content()
    try:
        old_price = await page.locator('del[class="sale-price__old"]').text_content(timeout=5000)
    except TimeoutError:
        old_price = '-'
    new_price = await page.locator('span[class="main-price"]').text_content(timeout=5000)
    if old_price == '-':
        price = new_price
        sale_price = old_price
    else:
        price = old_price
        sale_price = new_price
    try:
        producer = await page.locator('div[class="attributes-list_block"]', has_text='Торгова марка').locator('a').text_content(timeout=5000)
    except TimeoutError:
        producer = '-'
    data = {'shop':'Сільпо','name':product_name, 'price':price, 'sale_price':sale_price, 'producer':producer.strip(), 'url':page.url}
    await add_to_excel(data)

async def silpo_parsing_all(page:Page):
    data = await read_json('silpo.json')
    for item in data:
        await silpo_parsing_one(page, item)