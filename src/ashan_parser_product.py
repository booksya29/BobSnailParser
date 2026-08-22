import asyncio
import re
from excel_add import add_to_excel
from json_manager import read_json
from patchright.async_api import Page, TimeoutError, async_playwright

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

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    old_price = 0
    try:
        old_price_el = page.locator('div[class*="ProductPagePrice_price_old"], div[class*="price_old"], del').first
        raw_old = await old_price_el.text_content(timeout=2000)
        old_price = raw_old.strip() if raw_old else 0
    except Exception:
        old_price = 0

    actual_price = '-'
    try:
        actual_price_el = page.locator('div[class*="ProductPagePrice_price_actual"], div[class*="price_actual"], div[class*="ProductPagePrice"]').first
        raw_act = await actual_price_el.text_content(timeout=2000)
        actual_price = raw_act.strip() if raw_act else '-'
    except Exception:
        actual_price = '-'

    if not old_price or old_price == 0 or old_price == '-':
        price = actual_price
        sale_price = '-'
    else:
        price = old_price
        sale_price = actual_price

    producer = '-'
    try:
        producer_el = page.locator('table[class*="productDetails_features__table"] tr', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first
        producer_text = await producer_el.text_content(timeout=2000)
        if producer_text and ":" in producer_text:
            producer = producer_text.split(":", 1)[1].strip()
        else:
            producer = producer_text.strip() if producer_text else '-'
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
        'shop': 'Ашан',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod or '-',
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
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await ashan_parsing_one(page, 'https://auchan.ua/ua/natural-nye-jablochno-klubnichnye-konfety-bob-snail-ravlik-bob-60-g-672727-899562/?srsltid=AfmBOorucJW-LwK8yWiGepkyLnqSYXZjlQATW3jvqHWY9TgNtv6dWw5X')
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())