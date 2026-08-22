import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import add_json, read_json
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

async def silpo_parsing_one(page: Page, url: str):
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
        print(f"[Сільпо] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    old_price = '-'
    try:
        has_old = await page.locator('del[class*="sale-price__old"], del').count() > 0
        old_price_raw = await page.locator('del[class*="sale-price__old"], del').first.text_content(timeout=1000) if has_old else '-'
        old_price = old_price_raw.strip() if old_price_raw else '-'
    except Exception:
        old_price = '-'

    new_price = '-'
    try:
        new_price_raw = await page.locator('span[class*="main-price"], div[class*="product-price"]').first.text_content(timeout=2000)
        new_price = new_price_raw.strip() if new_price_raw else '-'
    except Exception:
        new_price = '-'

    if old_price and old_price != '-':
        price = old_price
        sale_price = new_price
    else:
        price = new_price
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await page.locator('div[class*="product-page__brand"] a, a[href*="/brand/"]').first.text_content(timeout=2000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Сільпо',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url
    }
    await add_to_excel(data)
    print(data)

async def silpo_parsing_all(page: Page, on_progress=None):
    data = await read_json('silpo.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await silpo_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Silpo item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await silpo_parsing_one(page,'https://silpo.ua/product/somga-shmatok-okholodzhenyi-878270')

if __name__ == "__main__":
    asyncio.run(test())