import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

async def fora_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return

    try:
        await page.wait_for_selector('h1[class="title"]', timeout=10000)
        raw_name = await page.locator('h1[class="title"]').text_content(timeout=5000)
        product_name = raw_name.strip() if raw_name else '-'
    except Exception:
        product_name = '-'

    price_container = page.locator('div[class*="product-price-container"]').first
    try:
        await page.wait_for_selector('div[class*="product-price-container"]', timeout=6000)
        price = await price_container.locator('div[class="old-integer"]').text_content(timeout=3000)
        sale_price_grn = await price_container.locator('div[class="current-integer"]').text_content(timeout=2000)
        sale_price_kop = await price_container.locator('div[class="current-fraction"]').text_content(timeout=2000)
        sale_price = f"{sale_price_grn}.{sale_price_kop}" if sale_price_grn and sale_price_kop else '-'
    except Exception:
        sale_price = '-'
        try:
            price_grn = await price_container.locator('div[class="current-integer"]').text_content(timeout=3000)
            price_kop = await price_container.locator('div[class="current-fraction"]').text_content(timeout=3000)
            price = f"{price_grn}.{price_kop}" if price_grn and price_kop else '-'
        except Exception:
            price = '-'

    try:
        await page.wait_for_selector('div[class*="product-details-column"]', timeout=5000)
        raw_producer = await page.locator('div[class="product-details-column trademark"]', has_text='Торгова марка').locator('div[class="product-details-value"]').text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Фора',
        'name': product_name,
        'price': price.strip() if isinstance(price, str) else str(price),
        'sale_price': sale_price.strip() if isinstance(sale_price, str) else str(sale_price),
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

async def fora_parsing_all(page: Page, on_progress=None):
    data = await read_json('fora.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await fora_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Fora item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)