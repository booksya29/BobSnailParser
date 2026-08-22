import asyncio
import re
from excel_add import add_to_excel
from patchright.async_api import Page, TimeoutError
from json_manager import read_json

def clean_p(v):
    if not v or v == '-' or v == 0 or v == '0':
        return '-'
    m = re.search(r'\d+[\.,]\d{2}|\d+', str(v).replace('\xa0', ' '))
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
                'закінчився',
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

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[АТБ] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    container = page.locator('div.js-product-container, div.cardproduct-popup, div[class*="product-about"], main').first

    price = '-'
    sale_price = '-'
    try:
        price_block = container.locator('div.product-price, div[class*="product-price"]').first
        is_sale = await price_block.locator('div[class*="product-price--sale"], div.product-price--sale').count() > 0 or await container.locator('div[class*="product-price--sale"]').count() > 0
        top_el = price_block.locator('data.product-price__top, [class*="product-price__top"], data, span.product-price__coin')
        bot_el = price_block.locator('data.product-price__bottom, [class*="product-price__bottom"]')
        top_p = await top_el.first.text_content(timeout=1000) if await top_el.count() > 0 else '-'
        bot_p = await bot_el.first.text_content(timeout=1000) if await bot_el.count() > 0 else '-'
        raw_p = await price_block.text_content(timeout=1000) if await price_block.count() > 0 else '-'
        
        if is_sale:
            price = bot_p if bot_p != '-' else top_p
            sale_price = top_p if bot_p != '-' else '-'
        else:
            if top_p != '-':
                price = top_p
            elif bot_p != '-':
                price = bot_p
            elif raw_p != '-':
                price = raw_p
            else:
                price = '-'
            sale_price = '-'
    except Exception:
        price = '-'
        sale_price = '-'

    producer = '-'
    try:
        raw_prod = await page.locator('div[class*="product-characteristics__item"]', has_text=re.compile(r'Торгова марка|Бренд|Виробник', re.I)).first.locator('div[class*="value"], span').first.text_content(timeout=1000)
        producer = raw_prod.strip() if raw_prod else '-'
    except Exception:
        producer = '-'

    data_row = {
        'shop': 'АТБ',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url
    }
    await add_to_excel(data_row)
    print(data_row)

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