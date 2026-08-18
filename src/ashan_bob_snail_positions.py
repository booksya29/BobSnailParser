from patchright.async_api import Page, async_playwright, TimeoutError
import asyncio
from json_manager import add_json

SEARCH_URL = 'https://express.auchan.ua/search/Bob%20SNail/'

async def ashan_bob_snail_products(page: Page):
    urls_list = []
    try:
        await page.goto(SEARCH_URL, wait_until='domcontentloaded', timeout=20000)
    except TimeoutError:
        print(f"Timeout loading {SEARCH_URL}")
        return urls_list
    except Exception as e:
        print(f"Error loading {SEARCH_URL}: {e}")
        return urls_list

    while True:
        try:
            await page.locator('div[class="page-item__button"]').locator('button').click(timeout=10000)
            await asyncio.sleep(1)
        except TimeoutError:
            await asyncio.sleep(2.5)
            break
        except Exception as e:
            print(f"Pagination click ended or failed: {e}")
            break

    all_items_first = await page.locator('div[style="display:contents"]').all()
    all_items_second = await page.locator('div[style="display: contents;"]').all()
    all_items = all_items_first + all_items_second

    for item in all_items:
        try:
            link_loc = item.locator('a[class*="ProductCard_data__name"]').first
            if await link_loc.count() > 0:
                href = await link_loc.get_attribute('href')
                if href:
                    full_url = 'https://express.auchan.ua' + href if href.startswith('/') else href
                    urls_list.append(full_url)
        except Exception as e:
            print(f"Error extracting item link: {e}")

    if urls_list:
        await add_json(urls_list, 'ashan.json')
    return urls_list

async def test():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        page = await browser.new_page()
        await ashan_bob_snail_products(page)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())