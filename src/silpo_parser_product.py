import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import add_json, read_json
from excel_add import add_to_excel

async def silpo_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=15000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        raw_name = await page.locator('h1[data-autotestid="product-page__title"]').text_content(timeout=3000)
        product_name = raw_name.strip() if raw_name else '-'
    except TimeoutError:
        product_name = '-'

    try:
        old_price_raw = await page.locator('del[class="sale-price__old"]').text_content(timeout=3000)
        old_price = old_price_raw.strip() if old_price_raw else '-'
    except TimeoutError:
        old_price = '-'

    try:
        new_price_raw = await page.locator('span[class="main-price"]').text_content(timeout=3000)
        new_price = new_price_raw.strip() if new_price_raw else '-'
    except TimeoutError:
        new_price = '-'

    if old_price == '-':
        price = new_price
        sale_price = old_price
    else:
        price = old_price
        sale_price = new_price

    try:
        raw_producer = await page.locator('div[class="attributes-list_block"]', has_text='Торгова марка').locator('a').text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except TimeoutError:
        producer = '-'

    data = {
        'shop': 'Сільпо',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

async def silpo_parsing_all(page: Page):
    data = await read_json('silpo.json')
    if not data:
        return
    for item in data:
        try:
            await silpo_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Silpo item {item}: {e}")
        await asyncio.sleep(1)