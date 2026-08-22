import asyncio
import re
from patchright.async_api import Page, TimeoutError, async_playwright
from json_manager import read_json
from excel_add import add_to_excel

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

async def varus_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[Варус] Товар відсутній в наявності: {url} - пропуск.")
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

    price = '-'
    sale_price = '-'
    try:
        del_el = page.locator('div.m-product-mini-details del, div.product-page__price del, del.sf-price__old, del')
        ins_el = page.locator('div.m-product-mini-details ins, div.product-page__price ins, ins.sf-price__special, ins')
        reg_el = page.locator('span.sf-price__regular, div.product-page__price, div.sf-price')
        has_old_v = await del_el.count() > 0
        old_v = await del_el.first.text_content(timeout=1000) if has_old_v else '-'
        act_v = await ins_el.first.text_content(timeout=1000) if await ins_el.count() > 0 else (await reg_el.first.text_content(timeout=1000) if await reg_el.count() > 0 else '-')
        if has_old_v and old_v != '-':
            price = old_v
            sale_price = act_v
        else:
            price = act_v
            sale_price = '-'
    except Exception:
        price = '-'
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await page.locator('div[class*="characteristics"], div', has_text=re.compile(r'Бренд|Торгова марка|Виробник', re.I)).first.locator('div').nth(1).text_content(timeout=2000)
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
        await varus_parsing_one(page, 'https://varus.ua/pyure-yabluko-grusha-ravlik-bob-pauch-90g')
        await bw.close()

if __name__ == "__main__":
    asyncio.run(test())