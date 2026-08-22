import asyncio
from patchright.async_api import async_playwright, Page, TimeoutError
from json_manager import add_json, read_json
from excel_add import add_to_excel

async def silpo_parsing_one(page: Page, url: str):
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=25000)
    except TimeoutError:
        print(f"Can't load {url}")
        return
    except Exception as e:
        print(f"Error navigating to {url}: {e}")
        return

    try:
        await page.wait_for_selector('h1[data-autotestid="product-page__title"]', timeout=10000)
        raw_name = await page.locator('h1[data-autotestid="product-page__title"]').text_content(timeout=5000)
        product_name = raw_name.strip() if raw_name else '-'
    except Exception:
        product_name = '-'

    try:
        await page.wait_for_selector('del[class*="sale-price__old"]', timeout=3000)
        old_price_raw = await page.locator('del[class="sale-price__old"]').text_content(timeout=3000)
        old_price = old_price_raw.strip() if old_price_raw else '-'
    except Exception:
        old_price = '-'

    try:
        await page.wait_for_selector('span[class*="main-price"]', timeout=5000)
        new_price_raw = await page.locator('span[class="main-price"]').text_content(timeout=3000)
        new_price = new_price_raw.strip() if new_price_raw else '-'
    except Exception:
        new_price = '-'

    if old_price == '-':
        price = new_price
        sale_price = old_price
    else:
        price = old_price
        sale_price = new_price

    try:
        await page.wait_for_selector('div[class*="attributes-list_block"]', timeout=5000)
        raw_producer = await page.locator('div[class="attributes-list_block"]', has_text='Торгова марка').locator('a').text_content(timeout=3000)
        producer = raw_producer.strip() if raw_producer else '-'
    except Exception:
        producer = '-'

    data = {
        'shop': 'Сільпо',
        'name': product_name,
        'price': price,
        'sale_price': sale_price,
        'producer': producer,
        'url': page.url
    }
    await add_to_excel(data)

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
        await silpo_parsing_one(page,'https://silpo.ua/product/tsukerky-bob-snail-naturalni-iabluchno-malynovi-719651?gad_source=1&gad_campaignid=23578242656&gbraid=0AAAAAo7bnAI7lkChutemp7UUGsu0LuAGE&gclid=CjwKCAjw7p_UBhBlEiwAhpIs70Z_5z5cn4z_IPu7LdrBRI6CjPYgHgTG4oQtXuxVILb4By4AekgqVRoC8E0QAvD_BwE')

if __name__ == "__main__":
    asyncio.run(test())