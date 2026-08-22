from patchright.async_api import async_playwright, TimeoutError, Page
import asyncio
from excel_add import add_to_excel
from json_manager import read_json

async def fozzy_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        await page.wait_for_selector('div[class="product_name"]', timeout=10000)
        raw_name = await page.locator('div[class="product_name"]').text_content(timeout=5000)
        product_name = raw_name.strip() if raw_name else '-'
    except Exception:
        product_name = '-'

    try:
        await page.wait_for_selector('div[class*="price_container"]', timeout=6000)
        raw_old = await page.locator('div[class*="price_container"]').locator('span[class="old_price"]').first.text_content(timeout=3000)
        old_price = raw_old.strip() if raw_old else '-'
    except Exception:
        old_price = '-'

    try:
        raw_regular = await page.locator('div[class*="price_container"]').locator('span[class="regular_price"]').first.text_content(timeout=3000)
        regular_price = raw_regular.strip() if raw_regular else '-'
    except Exception:
        regular_price = '-'

    if old_price == '-':
        price = regular_price
        sale_price = old_price
    else:
        price = old_price
        sale_price = regular_price

    try:
        await page.wait_for_selector('div[class="product_characteristics_item"]', timeout=5000)
        raw_producer = await page.locator('div[class="product_characteristics_item"]', has_text='Бренд').locator('a').text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Фоззі',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

async def fozzy_parsing_all(page: Page, on_progress=None):
    data = await read_json('fozzy.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await fozzy_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Fozzy item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=False)
        page = await b.new_page()
        await fozzy_parsing_one(page, "https://fozzyshop.ua/skhidni-solodoshchi-khalva/950652-pastyla-fruktova-premiia-grusha-iabluko-ta-iabluko-persyk.html")
        await b.close()

if __name__ == "__main__":
    asyncio.run(test())