# Дніпро METRO (zakaz Дніпро) Дніпро  


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import asyncio
import re
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import read_json
from excel_add import add_to_excel

async def check_addr(page:Page) -> bool:
    try:
        await page.wait_for_selector('div[data-marker="Responsive_tablet_desktop"]')
        await asyncio.sleep(1)
        addr_name = (await page.locator('div[data-marker="Responsive_tablet_desktop"]').first.text_content()).strip()
        print(addr_name)
        if "Дніпро" in addr_name:
            return True
        else:
            set_b = await set_addr(page)
            return set_b
    except TimeoutError as e:
        print('check_addr -- ', e)
        return False
async def set_addr(page:Page) -> bool:
    try:
        await page.locator('span[class*="AddressButton"]').first.click() # Вибір адреси
        await page.locator('li[data-marker="Pickup"]').first.click() # Кнопка самовивозу
        await page.locator('div[class="SelectStyled__single-value css-r447wv-singleValue"]').nth(0).click() # nth 0 - населений пункт, nth 1 - місце видачі
        await page.locator('div[id*="react-select-"]', has_text='Дніпро').click() # Адреса в списку
        await page.locator('span[class*="Button__text"]', has_text='покуп').click() # Перейти до покупок
        await page.wait_for_load_state(state="domcontentloaded")
        return True
    except TimeoutError as e:
        print("set_addr -- ",e)
        return False
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


async def check_in_stock(page:Page) -> bool:
    try:
        if (await page.locator('div[class*="BigProductCardTopInfo__addToCartButtons"]').text_content()).strip() == "Немає в наявності":
            return False
        else:
            return True
    except TimeoutError:
        print(f"Помилка пошуку кнопки 'Додати до корзини'. --- {page.url}")
        return False
async def ashan_parsing_one(page: Page, url: str):
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
    check_addr_bool = await check_addr(page)
    if check_addr_bool == False:
        print('Не вдалося поміняти адресу магазина')
        return False
    
    product_name = '-'
    for _ in range(10):
        try:
            h1 = await page.locator('h1, div[class*="BigProductCardTopInfo__title"]').first.text_content(timeout=1000)
            if h1 and h1.strip():
                product_name = h1.strip()
                break
        except Exception:
            pass
        await asyncio.sleep(0.2)

    in_stock = await check_in_stock(page)
    if not in_stock:
        print(f"[Новус] Товар відсутній в наявності: {url} - пропуск.")
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(r' - | \| | купити', t)[0].strip()
        except Exception:
            product_name = '-'

    container = page.locator('div[data-marker="Big Product Cart"], div[class*="BigProductCard"], main').first
    price_info = container.locator('div[class*="BigProductCardTopInfo__priceInfo"], div[data-marker="Big Product Cart"]').first

    price = '-'
    sale_price = '-'
    try:
        old_el = price_info.locator('span[data-marker="Old Price"], div[data-marker="Old Price"]')
        act_el = price_info.locator('span[data-marker="Discounted Price"], span[data-marker="Price"], div[data-marker="Discounted Price"], div[data-marker="Price"]')
        has_old = await old_el.count() > 0
        old_val = await old_el.first.text_content(timeout=1000) if has_old else '-'
        act_val = await act_el.first.text_content(timeout=1000) if await act_el.count() > 0 else '-'

        if has_old and old_val and old_val != '-':
            price = old_val
            sale_price = act_val
        else:
            price = act_val
            sale_price = '-'
    except Exception:
        price = '-'
        sale_price = '-'

    producer = '-'
    try:
        raw_producer = await page.locator('li[data-marker*="tm"], li', has_text=re.compile(r'Бренд|ТМ|Виробник', re.I)).first.text_content(timeout=1000)
        if raw_producer and (":" in raw_producer or "\n" in raw_producer):
            parts = re.split(r'[:\n]+', raw_producer)
            producer = parts[-1].strip() if len(parts) > 1 else raw_producer.strip()
        else:
            producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    id = page.url.split('--')[1][1::].replace('/', '')
    data = {
        'shop': 'Дніпро Auchan (Дніпро) Дніпро',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url,
        'id':id
    }
    await add_to_excel(data)
    print(data)

async def ashan_parsing_all(page: Page, on_progress=None):
    data = await read_json('novus.json')
    if not data:
        if on_progress:
            on_progress(100)
        return
    total = len(data)
    for i, item in enumerate(data, start=1):
        try:
            await ashan_parsing_one(page, item)
        except Exception as e:
            print(f"Error parsing Novus item {item}: {e}")
        if on_progress:
            on_progress(int((i / total) * 100))
        await asyncio.sleep(1)

async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(headless=False)
        page = await bw.new_page()
        urls = ['https://metro.zakaz.ua/uk/products/m-iaso-nasha-riaba--metro28968100000000/', 'https://metro.zakaz.ua/uk/products/file-epikur--metro28798500000000/', 'https://metro.zakaz.ua/uk/products/proshutto-250g-italiia--08018896880271/']
        for i in urls:
            await ashan_parsing_one(page, i)
            await asyncio.sleep(1)
if __name__ == '__main__':
    asyncio.run(test())