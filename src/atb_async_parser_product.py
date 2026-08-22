import asyncio
import re
from excel_add import add_to_excel
from patchright.async_api import Page, TimeoutError
from json_manager import read_json

async def atb_parsing(page: Page, url: str):
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
        raw_bottom = await page.locator('data[class*="product-price__bottom"], div[class*="product-about__buy-row"] data').first.text_content(timeout=2000)
        sale_price = raw_bottom.strip() if raw_bottom else '-'
    except Exception:
        sale_price = '-'

    try:
        raw_top = await page.locator('data[class*="product-price__top"] span, data[class*="product-price__top"]').first.text_content(timeout=2000)
        price = raw_top.strip() if raw_top else '-'
    except Exception:
        price = '-'

    if price == '-' or not price:
        price = sale_price
        sale_price = '-'

    producer = '-'
    try:
        raw_prod = await page.locator('div[class*="product-characteristics__item"]', has_text=re.compile(r'Торгова марка|Бренд|Виробник', re.I)).first.locator('div[class*="value"], span').first.text_content(timeout=2000)
        producer = raw_prod.strip() if raw_prod else '-'
    except Exception:
        producer = '-'

    def clean_p(v):
        if not v or v == '-':
            return '-'
        m = re.search(r'\d+[\.,]\d{2}|\d+', str(v).replace('\xa0', ' '))
        return m.group(0).replace(',', '.') if m else str(v).strip()

    data_row = {
        'shop': 'АТБ',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': re.sub(r'^(Бренд|ТМ|Виробник|Торгова марка)\s*:?\s*', '', producer, flags=re.I).strip() or '-',
        'url': page.url
    }
    await add_to_excel(data_row)

async def atb_all_parsing(page: Page, on_progress=None):
    url_list = await read_json('atb.json')
    if not url_list:
        if on_progress:
            on_progress(100)
        return
    total = len(url_list)
    for i, url in enumerate(url_list, start=1):
        try:
            await atb_parsing(page, url)
        except Exception as e:
            print(f"Error parsing ATB item {url}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)