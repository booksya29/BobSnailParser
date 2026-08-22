import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

async def metro_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        await page.wait_for_selector('div[class="titleDisplay"] h2', timeout=10000)
        raw_name = await page.locator('div[class="titleDisplay"]').locator('h2').text_content(timeout=5000)
        product_name = raw_name.strip() if raw_name else '-'
    except Exception:
        product_name = '-'

    price_container = page.locator('div[class*="price-container"]')
    try:
        await page.wait_for_selector('div[class*="price-container"]', timeout=6000)
        sale_price_raw = await price_container.locator('span[class*="price-breakdown primary promotion"]').text_content(timeout=3000)
        price_raw = await price_container.locator('span[class*="price-breakdown strike"]').text_content(timeout=3000)
        sale_price = sale_price_raw if sale_price_raw else '-'
        price = price_raw if price_raw else '-'
    except Exception:
        sale_price = '-'
        try:
            price_reg = await price_container.locator('span[class*="price-breakdown primary"]').text_content(timeout=3000)
            price = price_reg if price_reg else '-'
        except Exception:
            price = '-'

    try:
        await page.wait_for_selector('div[class="mfcss_article-detail--overview"]', timeout=5000)
        raw_producer = await page.locator('div[class="mfcss_article-detail--overview"]').locator('p', has_text='Бренд').locator('span').nth(1).text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    clean_price = price.replace('\xa0грн  з ПДВ', '').replace('\xa0грн з ПДВ', '').strip() if isinstance(price, str) else str(price)
    clean_sale_price = sale_price.replace('\xa0грн  з ПДВ', '').replace('\xa0грн з ПДВ', '').strip() if isinstance(sale_price, str) else str(sale_price)

    data = {
        'shop': 'Метро',
        'name': product_name,
        'price': clean_price,
        'sale_price': clean_sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

async def metro_parsing_all(page: Page, on_progress=None):
    data = await read_json('metro.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await metro_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Metro item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await metro_parsing_one(page, 'https://shop.metro.ua/shop/pv/BTY-X342441/0032/0021/Bob-Snail-%D0%9D%D0%B0%D0%B1%D1%96%D1%80-%D0%A6%D1%83%D0%BA%D0%B5%D1%80%D0%BA%D0%B8-%D1%84%D1%80%D1%83%D0%BA%D1%82-%D0%AF%D0%B1%D0%BB%D1%83%D0%BA%D0%BE-%D0%B3%D1%80%D1%83%D1%88%D0%B0-20%D0%B3+%D1%96%D0%B3%D1%80%D0%B0%D1%88%D0%BA%D0%B0-1%D1%88%D1%82')
        await bw.close()

if __name__ == "__main__":
    asyncio.run(test())