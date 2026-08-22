import asyncio
import re
from patchright.async_api import Page, TimeoutError, async_playwright
from json_manager import read_json
from excel_add import add_to_excel

def clean_p(v):
    if not v or v == '-' or v == 0 or v == '0':
        return '-'
    s = re.sub(r'\s+', '', str(v).replace('\xa0', ' '))
    m = re.search(r'\d+[\.,]\d{2}|\d+', s)
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

async def varus_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    # 1. Hydrate Title (up to 6s)
    product_name = '-'
    for _ in range(30):
        try:
            h1 = await page.locator('h1, div.product__header').first.text_content(timeout=500)
            if h1 and h1.strip() and len(h1.strip()) > 3 and 'varus.ua' not in h1.lower():
                product_name = h1.strip()
                break
        except Exception:
            pass
        await asyncio.sleep(0.2)

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[Варус] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t and 'varus.ua' not in t.lower():
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    # 2. Extract Prices
    price = '-'
    sale_price = '-'
    try:
        res = await page.evaluate('''() => {
            const delEl = document.querySelector('div.m-product-short-info__price-section del, div.product-page__price del, del.sf-price__old, del');
            const insEl = document.querySelector('div.m-product-short-info__price-section ins, div.product-page__price ins, ins.sf-price__special, ins');
            const regEl = document.querySelector('div.m-product-short-info__price-section span.sf-price__regular, div.product-page__price .sf-price, span.sf-price__regular');
            return {
                old: delEl ? delEl.innerText : null,
                act: insEl ? insEl.innerText : (regEl ? regEl.innerText : null)
            };
        }''')
        old_p = res.get('old')
        act_p = res.get('act')
        if old_p and old_p != '-' and 'закінчився' not in str(old_p).lower():
            price = old_p
            sale_price = act_p if act_p else '-'
        else:
            price = act_p if act_p else '-'
            sale_price = '-'
    except Exception:
        price = '-'
        sale_price = '-'

    # 3. Extract Producer
    producer = '-'
    try:
        raw_producer = await page.locator('div[class*="characteristics"], div', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first.locator('div').nth(1).text_content(timeout=1000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Варус',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url
    }
    await add_to_excel(data)
    print(data)

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