import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import asyncio
import re
from excel_add import add_to_excel
from patchright.async_api import Page, TimeoutError, async_playwright
from json_manager import read_json
addr_dict = {
    '1':'вул. Григоровича-Барського, 1',
    '2':"вул. Лук'яненка Левка, буд. 21/2-прим.(гр.пр.)102,1",
    '3':"просп. Оболонський, 52 а"
    }

async def select_addr(page:Page):
    await asyncio.sleep(1)
    addr_name = await page.locator('button[class*="delivery-info__button"]').nth(0).text_content(timeout=2000)
    if 'Рудницького' in addr_name:
        return True
    await page.locator('div[class="top-header__store"]').nth(0).click(timeout=3000)
    await page.locator('span[class="city-modal__delivery-name"]', has_text='Самовивіз').click(timeout=3000)
    await page.locator('span[class*="select2-selection"][role="combobox"]').first.click(timeout=3000)
    await asyncio.sleep(1)
    await page.locator('li[class*="select2-results__option"]', has_text='Київ').first.click(timeout=3000)
    await page.locator('span[class="select2-selection select2-selection--single"]').nth(1).click(timeout=3000)
    await asyncio.sleep(1)
    await page.locator('li[class*="select2-results__option"]', has_text='Рудницького, 14').click(timeout=3000)
    await page.locator('button[class*="city-modal__submit"]').click(timeout=3000)

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
                'закінчився',
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
def addr_split(url:str):
    url_list = url.split('&&&')
    return url_list[0], url_list[1]

async def atb_parsing(page: Page, url: str):
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
        print(f"[АТБ] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    actual_price = '-'
    old_price = '-'
    await page.wait_for_selector('h1[class="page-title product-page__title"]', state='attached')
    block_price = page.locator('div[class="product-about__buy-row"]').first
    try:
        old_price = await block_price.locator('data[class="product-price__bottom"]').text_content(timeout=1000)
    except TimeoutError:
        old_price = '-'
    try:
        actual_price = await block_price.locator('data[class="product-price__top"]').text_content(timeout=1000)
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
        raw_prod = await page.locator('div[class*="product-characteristics__item"]', has_text=re.compile(r'Торгова марка|Бренд|Виробник', re.I)).first.locator('div[class*="value"], span').first.text_content(timeout=1000)
        producer = raw_prod.strip() if raw_prod else '-'
    except Exception:
        producer = '-'
    try:
        id_not_sep = await page.locator('span[class="custom-tag__text"]').first.text_content()
        id = (id_not_sep.split(':'))[1]
    except TimeoutError:
        id = '-'
    data_row = {
        'shop': 'АТБ',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url,
        'id':id.strip()
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


async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        urls = [
    "https://www.atbmarket.com/product/cukerki-v-sokoladi-30-g-bob-snail-naturalni-ablucno-polunicni-ablucno-malinovi-kup",
    "https://www.atbmarket.com/product/pure-200-g-elfik-agidnij-miks-dp",
    "https://www.atbmarket.com/product/pure-110-g-elfik-krem-sup-z-kurkou-dp",
    # "https://www.atbmarket.com/product/pure-90-g-galicia-baby-ablucno-grusevo-spinatne-dp",
    # "https://www.atbmarket.com/product/pure-90-g-cudo-cado-fruktovo-agidne-z-kaseu-zlakovou-vid-6-mis",
]


        for item in urls:
            await atb_parsing(page, item)
            await asyncio.sleep(1)
if __name__ == '__main__':
    asyncio.run(test())