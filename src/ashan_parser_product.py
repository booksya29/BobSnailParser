import asyncio
import re
from excel_add import add_to_excel
from json_manager import read_json
from patchright.async_api import Page, TimeoutError, async_playwright

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
        status = await page.locator('div[class*="product_product__status"]').text_content(timeout=2500)
        print(status)
        if status.strip() == 'Немає в наявності':
            return False
        else: 
            return True
    except:
        return False
async def ashan_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
    except TimeoutError:
        print(f"Can't connect to {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    # 1. Hydrate Title (up to 6s)
    product_name = '-'
    for _ in range(30):
        try:
            h1 = await page.locator('h1').first.text_content(timeout=500)
            if h1 and h1.strip() and len(h1.strip()) > 3:
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

    container = page.locator('div[class*="ProductPage_productPage"], main').first
    price_wrap = container.locator('div[class*="ProductPagePrice_priceWrapper"], div[class*="ProductPage_price"], div[class*="product_product__price"]').first

    old_price = '-'
    actual_price = '-'
    try:
        old_price = await page.locator('div[class*="ProductPagePrice_price_old"]').text_content(timeout=5000)
    except TimeoutError:
        old_price = '-'
    try:
        actual_price = await page.locator('div[class*="ProductPagePrice_price_actual"]').text_content(timeout=5000)
    except TimeoutError:
        actual_price = '-'
    if old_price == '-':
        sale_price = '-'
        price = actual_price
    else:
        sale_price = actual_price
        price = old_price
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


async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        await ashan_parsing_one(page,"https://auchan.ua/ua/pjure-fruktovo-jagodnoe-banan-chernika-bob-snail-d-p-400g-691839/")
        await ashan_parsing_one(page, 'https://auchan.ua/ua/detskoe-pjure-gerber-chernosliv-80-g-258087/')
if __name__ == '__main__':
    asyncio.run(test())