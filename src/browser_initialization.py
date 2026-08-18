import asyncio
from patchright.async_api import async_playwright
from atb_async_parser_product import atb_parsing
from excel_add import add_to_excel
from atb_parser_positions import start_parsing_atb_positions

async def main():
    try:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=False)
            context = await browser.new_context(viewport={'height': 1080, 'width': 1920})
            page_atb = await context.new_page()
            atb_urls = await start_parsing_atb_positions(page_atb)
            for url in atb_urls:
                try:
                    await atb_parsing(page_atb, url)
                except Exception as e:
                    print(f"Error parsing {url}: {e}")
                await asyncio.sleep(1)
            await browser.close()
    except Exception as e:
        print(f"Browser main error: {e}")

if __name__ == "__main__":
    asyncio.run(main())