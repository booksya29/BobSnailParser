import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel_new
async def select_addr(page:Page):
    addr_name = (await page.locator('li[class="header-info-item location is_not_mobile"]').text_content()).strip()
    if "Берестейський" in addr_name:
        return True
    await page.locator('li[class*="header-info-item location"]').click(timeout=3000)
    await page.locator('div[class*="button-switch"]', has_text='Самовивіз').nth(1).click(timeout=3000)
    await asyncio.sleep(1)
    await page.locator('div[class="store-select__autocomplete-holder-store"]').click(timeout=3000, click_count=2)
    await asyncio.sleep(1)
    await page.locator('div[class="store-select__autocomplete-item"]', has_text='Берестейський').click(timeout=3000, click_count=2)
    await page.locator('a[class="btn btn-primary reversed confirm-btn-mobile"]').click(timeout=3000)
    await asyncio.sleep(1.5)
    
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
            const text = (document.querySelector('div.product-page, div[class*="product-details"], main')?.innerText || '').toLowerCase();
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

async def fora_parsing_one(page: Page, url: str):
    for _ in range(3):
        try:
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_selector('h1', timeout=15000)
            break
        except TimeoutError:
            print(f"Can't load {url}")
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
        await asyncio.sleep(3)
    else:
        return
    await select_addr(page)
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
        print(f"[Фора] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    container = page.locator('div.product-page, div[class*="product-details"], main').first
    price_wrap = container.locator('div.product-price-container, div.current-price').first

    price = '-'
    sale_price = '-'
    try:
        old_el = price_wrap.locator('div.old-price, div.old-integer')
        curr_grn_el = price_wrap.locator('div.current-integer')
        curr_kop_el = price_wrap.locator('div.current-fraction')
        old_val = await old_el.first.text_content(timeout=1000) if await old_el.count() > 0 else ''
        curr_grn = await curr_grn_el.first.text_content(timeout=1000) if await curr_grn_el.count() > 0 else ''
        curr_kop = await curr_kop_el.first.text_content(timeout=1000) if await curr_kop_el.count() > 0 else ''

        curr_price = f"{curr_grn.strip()}.{curr_kop.strip()}" if curr_grn and curr_kop else (curr_grn.strip() if curr_grn else '-')
        if old_val and old_val.strip() and old_val != '-':
            price = old_val
            sale_price = curr_price
        else:
            price = curr_price
            sale_price = '-'
    except Exception:
        price = '-'
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await container.locator('div[class*="trademark"], div[class*="product-details-column"]', has_text=re.compile(r'Торгова марка|Бренд', re.I)).first.locator('div[class*="value"], a, span').first.text_content(timeout=1000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    try:
        id_not_sep = await page.locator('div[class="article-number"]').text_content()
        id = id_not_sep.split(':')[1].strip()
    except TimeoutError:
        id = '-'
    data = {
        'shop': 'Фора',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url,
        'id':id,
        'Адреса': 'Київ. Берестейський 60'
    }
    await add_to_excel_new(data)
    print(data)

async def fora_parsing_all(page: Page, on_progress=None):
    data = await read_json('kyiv_fora_berest.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await fora_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Fora item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        urls = ['https://fora.ua/product/voda-mineralna-borjomi-sylnogazovana-sklo-1008', 'https://fora.ua/product/gorilka-finlandia-37541', 'https://fora.ua/product/nektaryn-45823' ]
        for i in urls:
            await fora_parsing_one(page, i)
            await asyncio.sleep(1)
if __name__ == '__main__':
    asyncio.run(test())
    