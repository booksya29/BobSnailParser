import asyncio
import sys
import io
from patchright.async_api import async_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

async def test():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(headless=False)
        context = await b.new_context(viewport={"height": 1, "width": 1})
        page = await context.new_page()

        urls = [
            "https://auchan.ua/ua/natural-nye-jablochno-klubnichnye-konfety-bob-snail-ravlik-bob-60-g-672727-899562/?srsltid=AfmBOorucJW-LwK8yWiGepkyLnqSYXZjlQATW3jvqHWY9TgNtv6dWw5X",
            "https://novus.zakaz.ua/uk/products/tsukerka-bob-sneil-60g--04820162520187/",
            "https://www.tavriav.ua/p/%D1%86%D1%83%D0%BA%D0%B5%D1%80%D0%BA%D0%B8-%D1%80%D0%B0%D0%B2%D0%BB%D0%B8%D0%BA-%D0%B1%D0%BE%D0%B1-%D1%8F%D0%B1%D0%BB%D1%83%D0%BA%D0%BE-30-%D0%B3-1574881"
        ]

        for u in urls:
            print(f"\n--- URL: {u} ---")
            await page.goto(u, wait_until="domcontentloaded")
            await asyncio.sleep(2)
            page_title = await page.title()
            print("Page Title:", page_title)
            all_h1 = await page.locator("h1").all_text_contents()
            print("H1 text contents:", all_h1)
            all_h1_inner = await page.evaluate("() => Array.from(document.querySelectorAll('h1')).map(e => e.innerText || e.textContent)")
            print("H1 via JS:", all_h1_inner)

        await b.close()

if __name__ == "__main__":
    asyncio.run(test())
