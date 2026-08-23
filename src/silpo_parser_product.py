import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import add_json, read_json
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
            const text = (document.querySelector('div[class*="product-page__content"], div.product-page, main')?.innerText || '').toLowerCase();
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
                if (text.includes(m)) return false;
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
            h1 = await page.locator('h1').first.text_content(timeout=500)
            if h1 and h1.strip() and len(h1.strip()) > 3:
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

    container = page.locator('div[class*="product-page__content"], div.product-page, main').first
    price_wrap = container.locator('div.prices-row, div[class*="product-page__price"], div.product-price').first

    actual_price = '-'
    old_price = '-'
    block_price = page.locator('div[class="prices-row"]')
    await page.wait_for_selector('div[class="prices-row"]', state='attached')
    try:
        actual_price = await block_price.locator('span[data-autotestid="product-main-price"]').text_content(timeout=2500)
    except TimeoutError:
        actual_price = '-'

    try: 
        old_price = await block_price.locator('del[data-autotestid="product-price-old"]').text_content(timeout=2500)
    except TimeoutError:
        old_price = '-'

    if old_price == '-':
        price = actual_price
        sale_price = '-'
    else:
        price = old_price
        sale_price = actual_price

    producer = '-'
    try:
        producer_block = page.locator('div[class="mat-expansion-panel-body"]')
        producer = await producer_block.locator('div[class="attributes-list_block"]', has_text='Торгова марка').locator('a').text_content(timeout=2500)
    except TimeoutError:
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
        silpo_urls = [
    "https://silpo.ua/product/piure-gerber-iabluko-morkva-garbuz-931700",
    "https://silpo.ua/product/smuzi-jaffa-z-bananiv-iabluk-chornytsi-ta-polunytsi-peretertykh-zi-zlakamy-743770",
]
        for url in silpo_urls:
            await silpo_parsing_one(page, url)
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(test())