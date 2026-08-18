import asyncio
from excel_add import add_to_excel
from json_manager import read_json
from patchright.async_api import Page, TimeoutError, async_playwright

async def ashan_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
    except TimeoutError:
        print(f"Can't connect to {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        raw_name = await page.locator('h1[class*=product_title]').first.text_content(timeout=3000)
        product_name = raw_name.strip() if raw_name else '-'
    except TimeoutError:
        product_name = '-'

    try:
        old_price = await page.locator('div[class *= "ProductPagePrice_price_old"]').text_content(timeout=1000)
    except TimeoutError:
        old_price = 0

    try:
        actual_price = await page.locator('div[class*="ProductPagePrice_price_actual"]').text_content(timeout=1000)
    except TimeoutError:
        actual_price = '-'

    if old_price == 0:
        price = actual_price
        sale_price = '-'
    else:
        price = old_price
        sale_price = actual_price

    try:
        producer_non_form = await page.locator('table[class*="productDetails_features__table"]').locator('tr', has_text='Бренд').text_content(timeout=1000)
        if producer_non_form and ":" in producer_non_form:
            producer_split = producer_non_form.split(":")
            producer = producer_split[1].strip()
        else:
            producer = producer_non_form.strip() if producer_non_form else 'NULL'
    except TimeoutError:
        producer = 'NULL'

    formatted_price = price.replace('\xa0', '').replace('грн', '').strip() if isinstance(price, str) else str(price)
    formatted_sale_price = sale_price.replace('\xa0', '').replace('грн', '').strip() if isinstance(sale_price, str) else (str(sale_price) if sale_price else None)

    data = {
        'shop': 'Ашан',
        'name': product_name,
        'price': formatted_price,
        'sale_price': formatted_sale_price,
        'producer': producer,
        'url': page.url,
    }
    await add_to_excel(data)

async def ashan_parsing_all(page: Page):
    data = await read_json('ashan.json')
    if not data:
        return
    for item in data:
        try:
            await ashan_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Ashan item {item}: {e}")
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await ashan_parsing_all(page)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())