from patchright.async_api import Page
from json_manager import add_json
URL = "https://www.atbmarket.com/catalog/trademark/7903?store=1154"


async def start_parsing_atb_positions(page: Page):
    atb_urls = []
    await page.goto(URL, wait_until="domcontentloaded")

    items_locator = page.locator(".catalog-list .catalog-item, .catalog-list article")
    await items_locator.first.wait_for(state="visible", timeout=10000)

    products = await items_locator.all()

    for item in products:
        link = item.locator("a.catalog-item__photo-link, a.catalog-item__title")

        if await link.count() > 0:
            href = await link.first.get_attribute("href")
            full_url = (
                f"https://www.atbmarket.com{href}"
                if href and href.startswith("/")
                else href
            )
            atb_urls.append(full_url)
    add_json(atb_urls)