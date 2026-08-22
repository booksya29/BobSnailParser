import asyncio
import re
from excel_add import add_to_excel
from json_manager import read_json
from patchright.async_api import Page, TimeoutError, async_playwright

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

async def ashan_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=25000)
    except TimeoutError:
        print(f"Can't connect to {url}")
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
        print(f"[Ашан] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    container = page.locator('div[class*="ProductPage_productPage"], main, body').first
    price_wrap = container.locator('div[class*="ProductPagePrice_priceWrapper"], div[class*="ProductPage_price"], div[class*="product_product__price"]').first

    old_price = '-'
    actual_price = '-'
    try:
        old_el = price_wrap.locator('div[class*="ProductPagePrice_price_old"]')
        has_old = await old_el.count() > 0
        old_price = await old_el.first.text_content(timeout=1000) if has_old else '-'
    except Exception:
        old_price = '-'

    try:
        act_el = price_wrap.locator('div[class*="ProductPagePrice_price_actual"]')
        has_act = await act_el.count() > 0
        actual_price = await act_el.first.text_content(timeout=1000) if has_act else '-'
    except Exception:
        actual_price = '-'

    if old_price and old_price != '-' and old_price != '0':
        price = old_price
        sale_price = actual_price
    else:
        price = actual_price
        sale_price = '-'

    producer = '-'
    try:
        producer_el = container.locator('table[class*="productDetails_features__table"] tr', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first
        producer_text = await producer_el.text_content(timeout=1000)
        if producer_text and ":" in producer_text:
            producer = producer_text.split(":", 1)[1].strip()
        else:
            producer = producer_text.strip() if producer_text else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Ашан',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url,
    }
    await add_to_excel(data)
    print(data)

async def ashan_parsing_all(page: Page, on_progress=None):
    data = await read_json('ashan.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await ashan_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Ashan item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)