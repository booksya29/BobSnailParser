import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

async def fora_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error loading {url}: {e}")
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
        price_container = page.locator('div[class*="product-price-container"], div[class*="price"]').first
        old_val = ''
        try:
            old_val = await price_container.locator('div[class*="old-integer"]').first.text_content(timeout=1000)
        except Exception:
            old_val = ''

        curr_grn = ''
        curr_kop = ''
        try:
            curr_grn = await price_container.locator('div[class*="current-integer"]').first.text_content(timeout=1000)
            curr_kop = await price_container.locator('div[class*="current-fraction"]').first.text_content(timeout=1000)
        except Exception:
            curr_grn = ''
            curr_kop = ''

        curr_price = f"{curr_grn.strip()}.{curr_kop.strip()}" if curr_grn and curr_kop else (curr_grn.strip() if curr_grn else '-')
        if old_val and old_val.strip():
            price = old_val.strip()
            sale_price = curr_price
        else:
            price = curr_price
            sale_price = '-'
    except Exception:
        price = '-'
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await page.locator('div[class*="trademark"], div[class*="product-details-column"]', has_text=re.compile(r'Торгова марка|Бренд', re.I)).first.locator('div[class*="value"], a, span').first.text_content(timeout=2000)
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
        'shop': 'Фора',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod or '-',
        'url': page.url
    }
    await add_to_excel(data)

async def fora_parsing_all(page: Page, on_progress=None):
    data = await read_json('fora.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await fora_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Fora item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)