import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

async def novus_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        await page.wait_for_selector('h1[data-marker="Big Product Cart Title"]', timeout=10000)
        raw_name = await page.locator('h1[data-marker="Big Product Cart Title"]').text_content(timeout=5000)
        product_name = raw_name.strip() if raw_name else '-'
    except Exception:
        product_name = '-'

    try:
        await page.wait_for_selector('span[data-marker="Old Price"]', timeout=4000)
        raw_price = await page.locator('span[data-marker="Old Price"]').text_content(timeout=3000)
        price = raw_price.strip() if raw_price else '-'
    except Exception:
        price = '-'

    try:
        await page.wait_for_selector('span[data-marker="Discounted Price"]', timeout=5000)
        raw_sale = await page.locator('span[data-marker="Discounted Price"]').text_content(timeout=3000)
        sale_price = raw_sale.strip() if raw_sale else '-'
    except Exception:
        sale_price = '-'

    try:
        await page.wait_for_selector('li[data-marker="Taxon tm"]', timeout=5000)
        raw_producer = await page.locator('li[data-marker="Taxon tm"]').locator('span').nth(1).text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Новус',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)
    print(data)

async def novus_parsing_all(page: Page, on_progress=None):
    data = await read_json('novus.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await novus_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Novus item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await novus_parsing_one(page, 'https://novus.zakaz.ua/uk/products/tsukerka-bob-sneil-60g--04820162520187/')

if __name__ == '__main__':
    asyncio.run(test())