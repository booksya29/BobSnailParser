import asyncio
import re
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
        raw_old = await page.locator('span[data-marker="Old Price"]').first.text_content(timeout=2000)
        old_val = raw_old.replace('\xa0грн', '').replace('грн', '').strip() if raw_old else '-'
    except Exception:
        old_val = '-'

    try:
        raw_sale = await page.locator('span[data-marker="Discounted Price"], span[data-marker="Price"]').first.text_content(timeout=2000)
        act_val = raw_sale.replace('\xa0грн', '').replace('грн', '').strip() if raw_sale else '-'
    except Exception:
        act_val = '-'

    if old_val and old_val != '-':
        price = old_val
        sale_price = act_val
    else:
        price = act_val
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await page.locator('li[data-marker*="tm"], li', has_text=re.compile(r'Бренд|ТМ|Виробник', re.I)).first.text_content(timeout=2000)
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

    data = {
        'shop': 'Новус',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': re.sub(r'^(Бренд|ТМ|Виробник|Торгова марка)\s*:?\s*', '', producer, flags=re.I).strip() or '-',
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