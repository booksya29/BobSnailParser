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

async def metro_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=30000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
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

    price = '-'
    sale_price = '-'
    producer = '-'

    if "zakaz.ua" in url:
        container = page.locator('div[data-marker="Big Product Cart"], div[class*="BigProductCard"], main, body').first
        price_info = container.locator('div[class*="BigProductCardTopInfo__priceInfo"], div[data-marker="Big Product Cart"]').first
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

        try:
            raw_producer = await page.locator('li[data-marker*="tm"], li', has_text=re.compile(r'Бренд|ТМ|Виробник', re.I)).first.text_content(timeout=1000)
            if raw_producer and (":" in raw_producer or "\n" in raw_producer):
                parts = re.split(r'[:\n]+', raw_producer)
                producer = parts[-1].strip() if len(parts) > 1 else raw_producer.strip()
            else:
                producer = raw_producer.strip() if raw_producer else '-'
        except Exception:
            producer = '-'
    else:
        try:
            res = await page.evaluate('''() => {
                const rightCol = document.querySelector('div.ev-productview-details--right-col, div[class*="article-detail"], main') || document.body;
                const strikeEl = rightCol.querySelector('span.strike, span[class*="strike"]');
                const promoEl = rightCol.querySelector('span.promotion, span[class*="promotion"]');
                const primaryEl = rightCol.querySelector('span.primary, span[class*="primary"], div.mfcss_article-detail--price-container');
                
                let brand = '-';
                const brandHeader = Array.from(rightCol.querySelectorAll('*')).find(e => e.innerText && e.innerText.trim() === 'Бренд');
                if (brandHeader && brandHeader.nextElementSibling) {
                    brand = brandHeader.nextElementSibling.innerText.trim();
                }

                return {
                    strike: strikeEl ? strikeEl.innerText : null,
                    promo: promoEl ? promoEl.innerText : null,
                    primary: primaryEl ? primaryEl.innerText : null,
                    brand
                };
            }''')

            strike = res.get('strike')
            promo = res.get('promo')
            primary = res.get('primary')
            producer = res.get('brand', '-')

            if strike and promo:
                price = strike
                sale_price = promo
            elif promo:
                price = promo
                sale_price = '-'
            else:
                price = primary if primary else '-'
                sale_price = '-'
        except Exception:
            price = '-'
            sale_price = '-'
            producer = '-'

    data = {
        'shop': 'Метро',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url
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