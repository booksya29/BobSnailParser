import asyncio
import re
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

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    price = '-'
    sale_price = '-'
    try:
        price_block = page.locator('div[class*="cart__actions__price"], div[class*="price"]').first
        p_raw = await price_block.text_content(timeout=2000)
        price = p_raw.replace('Додати', '').replace('₴', '').strip() if p_raw else '-'
    except Exception:
        price = '-'

    producer = '-'
    try:
        producer_el = page.locator('table tr, div[class*="feature"]', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first
        raw_producer = await producer_el.text_content(timeout=2000)
        if raw_producer and (":" in raw_producer or "\n" in raw_producer):
            parts = re.split(r'[:\n]+', raw_producer)
            producer = parts[-1].strip() if len(parts) > 1 else raw_producer.strip()
        else:
            producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    def clean_p(v):
        if not v or v == '-':
            return '-'
        m = re.search(r'\d+[\.,]\d{2}|\d+', str(v).replace('\xa0', ' '))
        return m.group(0).replace(',', '.') if m else str(v).strip()

    clean_prod = re.sub(r'^(Бренд|ТМ|Виробник|Торгова марка)\s*:?\s*', '', producer, flags=re.I).strip()
    if len(clean_prod) > 40:
        clean_prod = '-'

    data = {
        'shop': 'Таврія',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod or '-',
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