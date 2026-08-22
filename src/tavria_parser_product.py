import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from excel_add import add_to_excel
from json_manager import read_json

async def tavria_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        await page.wait_for_selector('h1[data-testid="detail-name"]', timeout=10000)
        raw_name = await page.locator('h1[data-testid="detail-name"]').text_content(timeout=5000)
        product_name = raw_name.strip() if raw_name else '-'
    except Exception:
        product_name = '-'

    price_block = page.locator('div[class*="cart__actions__price"]').first
    try:
        await page.wait_for_selector('div[class*="cart__actions__price"]', timeout=6000)
        price_unform = await price_block.locator('p[data-testid*="crossed-out-old"]').text_content(timeout=3000)
        sale_price = await price_block.locator('p[class*="base__price"]').text_content(timeout=3000)
    except Exception:
        try:
            price_unform = await price_block.text_content(timeout=3000)
        except Exception:
            price_unform = '-'
        sale_price = '-'

    price = price_unform.replace('Додати', '').strip() if price_unform else '-'
    sale_price = sale_price.replace('Додати', '').strip() if sale_price else '-'
    producer = '-'

    data = {
        'shop': 'Таврія',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

async def tavria_parsing_all(page: Page, on_progress=None):
    data = await read_json('tavria.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await tavria_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Tavria item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)