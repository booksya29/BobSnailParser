import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

def clean_p(v):
    if not v or v == '-' or v == 0 or v == '0':
        return '-'
    m = re.search(r'\d+[\.,]\d{2}|\d+', str(v).replace('\xa0', ' '))
    return m.group(0).replace(',', '.') if m else str(v).strip()

def clean_prod(v):
    if not v or v == '-' or v == 'NULL':
        return '-'
    cleaned = re.sub(r'^(Бренд|ТМ|Виробник|Торгова марка)\s*:?\s*', '', str(v), flags=re.I).strip()
    return cleaned if len(cleaned) <= 40 else '-'

async def check_in_stock(page: Page) -> bool:
    try:
        res = await page.evaluate('''() => {
            const body = (document.body.innerText || '').toLowerCase();
            const markers = [
                'немає в наявності',
                'немає на складі',
                'товар закінчився',
                'цей товар закінчився',
                'закінчився',
                'повідомити про наявність',
                'повідомити, коли з’явиться',
                'повідомити коли з’явиться',
                'тимчасово відсутній'
            ];
            for (const m of markers) {
                if (body.includes(m)) return false;
            }
            const outEl = document.querySelector('[data-marker*="Out of Stock"], [data-marker*="outOfStock"], .out-of-stock, [class*="not-available"]');
            if (outEl) return false;
            return true;
        }''')
        return bool(res)
    except Exception:
        return True

async def metro_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    product_name = '-'
    for _ in range(10):
        try:
            h1 = await page.locator('h1').first.text_content(timeout=1000)
            if h1 and h1.strip():
                product_name = h1.strip()
                break
        except Exception:
            pass
        await asyncio.sleep(0.2)

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[Метро] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    price = '-'
    sale_price = '-'
    producer = '-'

    if "zakaz.ua" in url:
        try:
            has_old = await page.locator('span[data-marker="Old Price"], div[data-marker="Old Price"]').count() > 0
            old_val = await page.locator('span[data-marker="Old Price"], div[data-marker="Old Price"]').first.text_content(timeout=1000) if has_old else '-'
            act_val = await page.locator('span[data-marker="Discounted Price"], span[data-marker="Price"], div[data-marker="Discounted Price"], div[data-marker="Price"]').first.text_content(timeout=1000) if await page.locator('span[data-marker="Discounted Price"], span[data-marker="Price"], div[data-marker="Discounted Price"], div[data-marker="Price"]').count() > 0 else '-'

            if has_old and old_val and old_val != '-':
                price = old_val
                sale_price = act_val
            else:
                price = act_val
                sale_price = '-'
        except Exception:
            price = '-'
            sale_price = '-'

        try:
            raw_producer = await page.locator('li[data-marker*="tm"], li', has_text=re.compile(r'Бренд|ТМ|Виробник', re.I)).first.text_content(timeout=2000)
            if raw_producer and (":" in raw_producer or "\n" in raw_producer):
                parts = re.split(r'[:\n]+', raw_producer)
                producer = parts[-1].strip() if len(parts) > 1 else raw_producer.strip()
            else:
                producer = raw_producer.strip() if raw_producer else '-'
        except Exception:
            producer = '-'
    else:
        price_container = page.locator('div[class*="price-container"]')
        try:
            sale_price_raw = await price_container.locator('span[class*="price-breakdown primary promotion"]').text_content(timeout=1000)
            price_raw = await price_container.locator('span[class*="price-breakdown strike"]').text_content(timeout=1000)
            sale_price = sale_price_raw if sale_price_raw else '-'
            price = price_raw if price_raw else '-'
        except Exception:
            sale_price = '-'
            try:
                price_reg = await price_container.locator('span[class*="price-breakdown primary"]').text_content(timeout=1000)
                price = price_reg if price_reg else '-'
            except Exception:
                price = '-'

        try:
            raw_producer = await page.locator('div[class*="mfcss_article-detail--overview"]').first.locator('span').nth(1).text_content(timeout=2000)
            producer = raw_producer.strip() if raw_producer else '-'
        except Exception:
            producer = '-'

    data = {
        'shop': 'Метро',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url
    }
    await add_to_excel(data)
    print(data)

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
        await metro_parsing_one(page, 'https://metro.zakaz.ua/ru/products/piure-bob-sneil-90g--04820219343042/')
        await bw.close()

if __name__ == "__main__":
    asyncio.run(test())