from patchright.async_api import Page, TimeoutError
from json_manager import add_json

URL = "https://www.atbmarket.com/catalog/trademark/7903?store=1154"

async def start_parsing_atb_positions(page: Page) -> list:
    atb_urls = []
    try:
        await page.goto(URL, wait_until="domcontentloaded", timeout=15000)
    except TimeoutError:
        print(f"Can't load {URL}")
        return atb_urls
    except Exception as e:
        print(f"Error navigating to {URL}: {e}")
        return atb_urls

    items_locator = page.locator(".catalog-list .catalog-item, .catalog-list article")
    try:
        await items_locator.first.wait_for(state="visible", timeout=10000)
    except TimeoutError:
        print("No ATB catalog items found within timeout")
        return atb_urls

    products = await items_locator.all()

    for item in products:
        try:
            link = item.locator("a.catalog-item__photo-link, a.catalog-item__title")
            if await link.count() > 0:
                href = await link.first.get_attribute("href")
                if href:
                    full_url = (
                        f"https://www.atbmarket.com{href}"
                        if href.startswith("/")
                        else href
                    )
                    atb_urls.append(full_url)
        except Exception as e:
            print(f"Error parsing ATB position item: {e}")

    if atb_urls:
        await add_json(atb_urls, 'atb.json')
    return atb_urls