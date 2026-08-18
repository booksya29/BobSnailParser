import asyncio
from excel_add import add_to_excel
from json_manager import read_json
from patchright.async_api import Page, TimeoutError, async_playwright
async def ashan_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until="domcontentloaded")
    except TimeoutError:
        print(f'Can`t connect to {page.url}')
        return
    product_name = await page.locator('h1[class*=product_title]').first.text_content()
    try:
        old_price = await page.locator('div[class *= "ProductPagePrice_price_old"]').text_content(timeout=1000)
    except TimeoutError:
        old_price = 0
    actual_price = await page.locator('div[class*="ProductPagePrice_price_actual"]').text_content(timeout=1000)
    if old_price == 0:
        price = actual_price
        sale_price = '-'
    else:
        price = old_price
        sale_price = actual_price
    try:
        producer_non_form = await page.locator('table[class*="productDetails_features__table"]').locator('tr', has_text='Бренд').text_content(timeout=1000)
        producer_split = producer_non_form.split(":")
        producer = producer_split[1]
    except TimeoutError as e:
        producer = 'NULL'
    data = {
    'shop': 'Ашан',
    'name': product_name,
    'price': price.replace('\xa0', '').replace('грн', '').strip(),
    'sale_price': sale_price.replace('\xa0', '').replace('грн', '').strip() if sale_price else None,
    'producer': producer,
    'url': page.url,}
    await add_to_excel(data)


async def ashan_parsing_all(page:Page):
    data = await read_json('ashan.json')
    if len(data) < 0:
        return
    for item in data: 
        await ashan_parsing_one(page, item)
        await asyncio.sleep(1)
async def test():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await ashan_parsing_all(page)

asyncio.run(test())