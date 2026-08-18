import asyncio
from patchright.async_api import Page, TimeoutError, async_playwright
from json_manager import read_json
from excel_add import add_to_excel

async def varus_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=15000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        raw_name = await page.locator('div[class="product__header"]').text_content(timeout=3000)
        product_name = raw_name.strip() if raw_name else '-'
    except TimeoutError:
        product_name = '-'

    price_block = page.locator('div[class="price"]')
    try:
        await page.wait_for_selector('div[class="price"]', timeout=3000)
        price_raw = await price_block.locator('del[class*="price__old"]').text_content(timeout=2000)
        sale_price_raw = await price_block.locator('ins[class*="sf-price__special"]').text_content(timeout=2000)
        price = price_raw.replace('₴', '').strip() if price_raw else '-'
        sale_price = sale_price_raw.replace('₴', '').strip() if sale_price_raw else '-'
    except TimeoutError:
        sale_price = '-'
        try:
            raw_reg = await price_block.locator('div[class="sf-price"]').text_content(timeout=2000)
            price = raw_reg.replace('₴', '').strip() if raw_reg else '-'
        except TimeoutError:
            price = '-'

    try:
        raw_producer = await page.locator('div[class="m-product-characteristics__row"]', has_text='Бренд').locator('div').nth(1).text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except TimeoutError:
        producer = '-'

    data = {
        'shop': 'Варус',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

async def varus_parsing_all(page: Page, on_progress=None):
    data = await read_json('varus.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await varus_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Varus item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await varus_parsing_one(page, 'https://varus.ua/cukerki-naturalni-yabluchni-bob-snail-60g')
        await bw.close()

if __name__ == "__main__":
    asyncio.run(test())