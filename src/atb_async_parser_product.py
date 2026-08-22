import asyncio
import re
from excel_add import add_to_excel
from patchright.async_api import Page, TimeoutError
from json_manager import read_json

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
        print(f"[АТБ] Товар відсутній в наявності: {url} - пропуск.")
        return

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
        res = await page.evaluate('''() => {
            const pb = document.querySelector('div.product-about__price, div.product-price');
            if (!pb) return { isSale: false, top: null, bot: null, text: null };
            const isSale = pb.classList.contains('product-price--sale') || !!pb.querySelector('.product-price--sale');
            const top = pb.querySelector('.product-price__top, data');
            const bot = pb.querySelector('.product-price__bottom');
            return {
                isSale,
                top: top ? top.innerText : null,
                bot: bot ? bot.innerText : null,
                text: pb.innerText
            };
        }''')
        is_sale = res.get('isSale', False)
        top_p = res.get('top')
        bot_p = res.get('bot')
        raw_t = res.get('text')
        
        if is_sale:
            price = bot_p if bot_p else top_p
            sale_price = top_p if bot_p else '-'
        else:
            price = top_p if top_p else (raw_t if raw_t else '-')
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