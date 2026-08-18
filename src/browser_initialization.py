from patchright.async_api import async_playwright
from atb_async_parser_product import atb_parsing
from excel_add import add_to_excel
import asyncio, os
from atb_parser_positions import start_parsing_atb_positions
async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'height':1980, 'width':1080})
        page_atb = await context.new_page()
        atb_urls = await start_parsing_atb_positions(page_atb)
        for url in atb_urls:
            await atb_parsing(page_atb, url)
        await browser.close()

asyncio.run(main())