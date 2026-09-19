import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import add_json, read_json
from excel_add import add_to_excel


async def select_addr(page:Page):
    await asyncio.sleep(1.5)
    addr_name = (await page.locator('div[class="header-delivery__body"]').text_content()).strip()
    print(addr_name)
    if 'Берестейський' in addr_name:
        return True
    await page.locator('button[class="header-delivery"]').click()
    await page.get_by_label('Самовивіз').click()
    try:
        await page.locator('i[class="ecomui-icon-cancel-circle icon"]').click()
    except:
        pass
    try:
        await page.locator('div[class*="search-input"]').first.click(timeout=2000)
    except:
        pass
    await asyncio.sleep(1)
    await page.locator('button[autotestid="\'search-suggestions__item\'"]', has_text = 'Київ').click(timeout=3000,click_count=2)
    await asyncio.sleep(1)
    await page.locator('div[data-autotestid="search-branch"]').click(timeout=3000, click_count=2)
    await asyncio.sleep(1)
    await page.locator('button[class*="search-suggestions__item ft-w-full"]', has_text='Берестейський, 94').click(timeout=3000, click_count=2)
    await page.locator('button[data-autotestid="self-delivery-submit-btn"]').click(timeout=3000)
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
    soldout_count = await page.locator('div[class="container"]').locator('output[data-autotestid="page-add-to-basket-soldout"]').count()
    if soldout_count != 0:
        return False
    return True

async def silpo_parsing_one(page: Page, url: str):
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