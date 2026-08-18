import asyncio
from excel_add import add_to_excel
from patchright.async_api import Page, TimeoutError
from json_manager import read_json
async def atb_parsing(page:Page, url:str):
    sale_price = 0
    await page.goto(url, wait_until='domcontentloaded')
    product_name = (await page.locator('div[class="product-about js-product-container"]').locator('h1').text_content(timeout=1000)).strip()
    try:
        price = (await page.locator('div[class="product-about__buy-row"]').first.locator('data[class="product-price__bottom"]').first.text_content(timeout=1000)).strip()
    except TimeoutError:
        sale_price = '-'
        print('Немає акції!')
    data = (await page.locator('data[class="product-price__top"]').locator('span').first.text_content(timeout=1000)).strip()
    if sale_price=='-':
        price=data
    else:
        sale_price=data
    try:
        producer = await page.locator('div[class="product-characteristics__item"]', has_text='Торгова марка').first.locator('div[class="product-characteristics__value"]').text_content(timeout=1000)
    except TimeoutError:
        print('Can`t find producer')
    data = {'shop':'АТБ','name':product_name, 'price':price, 'sale_price':sale_price, 'producer':producer.strip(), 'url':page.url}
    add_to_excel(data)

async def atb_all_parsing(page:Page):
    url_list = await read_json('atb.json')
    if url_list < 0:
        return
    for url in url_list:
        await atb_parsing(page, url)
        asyncio.sleep(1)