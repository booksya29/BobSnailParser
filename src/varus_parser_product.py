import asyncio
import re
from patchright.async_api import Page, TimeoutError, async_playwright
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
            const titleTop = document.querySelector('h1')?.getBoundingClientRect().top ?? 0;
            const isProductArea = el => {
                const r = el.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && r.top >= titleTop - 100 && r.top <= titleTop + 1200;
            };
            const text = Array.from(document.querySelectorAll(
                'button, [role="alert"], [class*="stock"], [class*="available"]'
            )).filter(isProductArea).map(el => el.innerText || '').join(' ').toLowerCase();
            const markers = [
                'немає в наявності',
                'немає на складі',
                'товар закінчився',
                'цей товар закінчився',
                'повідомити про наявність',
                'повідомити, коли з’явиться',
                'повідомити коли з’явиться',
                'тимчасово відсутній'
            ];
            for (const m of markers) {
                if (text.includes(m)) return false;
            }
            const outEl = Array.from(document.querySelectorAll(
                '[data-marker*="Out of Stock"], [data-marker*="outOfStock"], .out-of-stock, [class*="not-available"]'
            )).find(isProductArea);
            if (outEl) return false;
            return true;
        }''')
        return bool(res)
    except Exception:
        return True

async def varus_parsing_one(page: Page, url: str):
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
            h1 = await page.locator('h1, div.product__header').first.text_content(timeout=500)
            if h1 and h1.strip() and len(h1.strip()) > 3 and 'varus.ua' not in h1.lower():
                product_name = h1.strip()
                break
        except Exception:
            pass
        await asyncio.sleep(0.2)

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[Варус] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t and 'varus.ua' not in t.lower():
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    old_price = '-'
    actual_price = '-'
    block_price = page.locator('div[class="price"]').first
    print('Чекаю на selector')
    await page.wait_for_selector('div[class="price"], button[class="sf-button sf-button--outline btn-not-available"]', state='attached')
    print('Дочекався')
    try:
        old_price = await block_price.locator('del[class="sf-price__old"]').text_content(timeout=1000)
    except TimeoutError:
        old_price = '-'

    try:
        regular_price = await block_price.locator('span[class*="sf-price__regular"]').text_content(timeout=1000)
    except TimeoutError as e:
        print(e)
        regular_price = '-'

    try:
        actual_price = await block_price.locator('ins[class*="sf-price__special"]').text_content(timeout=1000)    
    except TimeoutError:
        actual_price = '-'


    if old_price == '-':
        price = regular_price
        sale_price = '-'
    else:
        price = old_price
        sale_price = actual_price
    producer = '-'
    try:
        raw_producer = await page.locator('div[class*="characteristics"], div', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first.locator('div').nth(1).text_content(timeout=1000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Варус',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url
    }
    await add_to_excel(data)
    print(data)

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

        await varus_parsing_one(page, url='https://varus.ua/marmelad-bob-snail-grusha-apelsin-v-belgijskom-molochnom-shokolade-naturalnyj-54-g')
        await varus_parsing_one(page, url='https://varus.ua/pyure-yabluko-grusha-ravlik-bob-pauch-90g')
if __name__ == '__main__':
    asyncio.run(test())