from patchright.async_api import Page, TimeoutError, async_playwright
import asyncio 
from json_manager import read_json
from excel_add import add_to_excel

async def varus_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load {page.url}')
        return
    product_name = await page.locator('div[class="product__header"]').text_content()
    price_block = page.locator('div[class="price"]')
    try:
        await page.wait_for_selector('div[class="price"]')
        price = await price_block.locator('del[class*="price__old"]').text_content(timeout=2000)
        sale_price = (await price_block.locator('ins[class*="sf-price__special"]').text_content(timeout=2000)).replace('₴', '')
    except TimeoutError as e:
        sale_price = '-'
        price = await price_block.locator('div[class="sf-price"]').text_content()
    producer = await page.locator('div[class="m-product-characteristics__row"]', has_text='Бренд').locator('div').nth(1).text_content()
    data = {'shop':'Варус','name':product_name.strip(), 'price':price.replace('₴', '').strip(), 'sale_price':sale_price.strip(), 'producer':producer.strip(), 'url':page.url}   
    print(data)
    await add_to_excel(data)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await varus_parsing_one(page, 'https://varus.ua/cukerki-naturalni-yabluchni-bob-snail-60g')

asyncio.run(test())