import asyncio
from excel_add import add_to_excel
from patchright.async_api import Page, TimeoutError
from json_manager import read_json

async def atb_parsing(page: Page, url: str):
    sale_price = 0
    price = '-'
    producer = '-'
    product_name = '-'
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=15000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        raw_name = await page.locator('div[class="product-about js-product-container"]').locator('h1').text_content(timeout=3000)
        product_name = raw_name.strip() if raw_name else '-'
    except TimeoutError:
        print(f"Can't find product name on {url}")

    try:
        raw_bottom = await page.locator('div[class="product-about__buy-row"]').first.locator('data[class="product-price__bottom"]').first.text_content(timeout=1000)
        price = raw_bottom.strip() if raw_bottom else '-'
    except TimeoutError:
        sale_price = '-'

    try:
        raw_top = await page.locator('data[class="product-price__top"]').locator('span').first.text_content(timeout=1000)
        data = raw_top.strip() if raw_top else '-'
    except TimeoutError:
        data = '-'

    if sale_price == '-':
        price = data
    else:
        sale_price = data

    try:
        raw_prod = await page.locator('div[class="product-characteristics__item"]', has_text='Торгова марка').first.locator('div[class="product-characteristics__value"]').text_content(timeout=1000)
        producer = raw_prod.strip() if raw_prod else '-'
    except TimeoutError:
        producer = '-'

    data_row = {
        'shop': 'АТБ',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data_row)

async def atb_all_parsing(page: Page, on_progress=None):
    url_list = await read_json('atb.json')
    if not url_list:
        if on_progress:
            on_progress(100)
        return
    total = len(url_list)
    for i, url in enumerate(url_list, start=1):
        try:
            await atb_parsing(page, url)
        except Exception as e:
            print(f"Error parsing ATB item {url}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)