import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
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
            const text = (document.querySelector('div[data-marker="Big Product Cart"], div[class*="BigProductCard"], div.ev-productview-details--right-col, main')?.innerText || '').toLowerCase();
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

async def metro_parsing_one(page: Page, url: str):
    for _ in range(3):
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_selector('h1, h2', timeout=15000)
            break
        except TimeoutError:
            print(f"Can't load {url}")
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
        await asyncio.sleep(3)
    else:
        return

    # 1. Hydrate Title (up to 8s)
    product_name = '-'
    for _ in range(40):
        try:
            h1 = await page.locator('h1, div.titleDisplay h2, div.mfcss_article-detail--title h2, div[class*="BigProductCardTopInfo__title"]').first.text_content(timeout=500)
            if h1 and h1.strip() and 'metro.ua' not in h1.lower() and len(h1.strip()) > 3:
                product_name = h1.strip()
                break
        except Exception:
            pass
        await asyncio.sleep(0.2)

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[Метро] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-' or product_name.lower() == 'metro.ua':
        try:
            t = await page.title()
            if t and 'metro.ua' != t.strip().lower():
                product_name = re.split(r' - | \| | купити', t)[0].replace('METRO', '').strip()
        except Exception:
            product_name = '-'

    old_price = '-'
    actual_price = ''
    block_price = page.locator('div[class*="price-container"]').first
    print('Почав чекати')
    await page.wait_for_selector('div[class*="price-container"]', state='attached')
    print('Закінчив')
    try:
        old_price = await block_price.locator('span[class*="price-breakdown strike"]').text_content(timeout=2500)
    except TimeoutError:
        old_price = '-'

    try:
        actual_price = await block_price.locator('span[class*="price-breakdown primary"], span[class*="price-breakdown primary promotion"]').first.text_content(timeout=2500)
    except TimeoutError:
        actual_price = '-'    

    if old_price == '-':
        price = actual_price
        sale_price = '-'
    else:
        price = old_price
        sale_price = actual_price

    producer = '-'    
    try:
        producer = await page.locator('div[class*="article-detail--overview"]').locator('p', has_text='Бренд').locator('span').nth(1).locator('span').text_content(timeout=2500)
    except TimeoutError:
        pass

    try: 
        id = await page.locator('div[class*="articlenumber"]').text_content()
    except TimeoutError:
        id = '-'
    data = {
        'shop': 'Метро',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url,
        'id':id.strip()
    }
    await add_to_excel(data)
    print(data)

async def metro_parsing_all(page: Page, on_progress=None):
    data = await read_json('metro.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await metro_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Metro item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        urls = ['https://shop.metro.ua/shop/pv/BTY-X382554/0032/0021/Bob-Snail-%D0%9F%D1%8E%D1%80%D0%B5-%D0%91%D0%B0%D0%BD%D0%B0%D0%BD-%D1%87%D0%BE%D1%80%D0%BD%D0%B0-%D1%81%D0%BC%D0%BE%D1%80%D0%BE%D0%B4%D0%B8%D0%BD%D0%B0-%D1%84%D1%80%D1%83%D0%BA%D1%82%D0%BE%D0%B2%D0%BE-%D1%8F%D0%B3%D1%96%D0%B4%D0%BD%D0%B5-120%D0%B3', 'https://shop.metro.ua/shop/pv/BTY-X382552/0032/0021/Bob-Snail-%D0%9F%D1%8E%D1%80%D0%B5-Smoothie-Banana-Raspberry-120%D0%B3', 'https://shop.metro.ua/shop/pv/BTY-X337476/0032/0021/Bob-Snail-%D0%9F%D1%8E%D1%80%D0%B5-%D0%A1%D0%BC%D1%83%D0%B7%D1%96-%D0%93%D1%80%D1%83%D1%88%D0%B0-%D0%BB%D1%96%D1%81%D0%BE%D0%B2%D0%B0-%D0%BE%D0%B6%D0%B8%D0%BD%D0%B0-%D1%84%D1%80%D1%83%D0%BA%D1%82%D0%BE%D0%B2%D0%BE-%D1%8F%D0%B3%D1%96%D0%B4%D0%BD%D0%B5-120%D0%B3']

        for i in urls:
            await metro_parsing_one(page, i)
if __name__ == '__main__':
    asyncio.run(test())
