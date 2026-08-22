import asyncio
import re
from patchright.async_api import Page, TimeoutError, async_playwright
from json_manager import read_json
from excel_add import add_to_excel

async def varus_parsing_one(page: Page, url: str):
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
            h1 = await page.locator('h1, div[class*="product__header"]').first.text_content(timeout=1000)
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

    old_price = '-'
    special_price = '-'
    try:
        price_block = page.locator('div[class*="product-page__price"], div[class="price"]').first
        old_el = await price_block.locator('del[class*="price__old"], del').first.text_content(timeout=2000)
        old_price = old_el.strip() if old_el else '-'
    except Exception:
        old_price = '-'

    try:
        price_block = page.locator('div[class*="product-page__price"], div[class="price"]').first
        act_el = await price_block.locator('ins[class*="sf-price__special"], ins, div[class*="sf-price"]').first.text_content(timeout=2000)
        special_price = act_el.strip() if act_el else '-'
    except Exception:
        special_price = '-'

    if old_price and old_price != '-':
        price = old_price
        sale_price = special_price
    else:
        price = special_price
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await page.locator('div[class*="characteristics"], div', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first.locator('div').nth(1).text_content(timeout=2000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    def clean_p(v):
        if not v or v == '-':
            return '-'
        m = re.search(r'\d+[\.,]\d{2}|\d+', str(v).replace('\xa0', ' '))
        return m.group(0).replace(',', '.') if m else str(v).strip()

    data = {
        'shop': 'Варус',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': re.sub(r'^(Бренд|ТМ|Виробник|Торгова марка)\s*:?\s*', '', producer, flags=re.I).strip() or '-',
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
        await varus_parsing_one(page, 'https://varus.ua/snek-bob-snail-yabluko-ta-grusha-17-g')
        await bw.close()

if __name__ == "__main__":
    asyncio.run(test())