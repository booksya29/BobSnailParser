from patchright.async_api import async_playwright, Page, TimeoutError
import asyncio
from json_manager import read_json
from excel_add import add_to_excel

async def novus_parsing_one(page:Page, url:str):
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except TimeoutError:
        print(f'Can`t load to {page.url}')
        return
    product_name = await page.locator('h1[data-marker="Big Product Cart Title"]').text_content()
    price = await page.locator('span[data-marker="Old Price"]').text_content(timeout=3000)
    try:
        sale_price = await page.locator('span[data-marker="Discounted Price"]').text_content(timeout=3000)
    except TimeoutError:
        sale_price = '-'
    try:
        producer = await page.locator('li[data-marker="Taxon tm"]').locator('span').nth(1).text_content(timeout=3000)
    except TimeoutError:
        producer = '-'

    data = {'shop':'Новус','name':product_name, 'price':price, 'sale_price':sale_price, 'producer':producer.strip(), 'url':page.url}
    await add_to_excel(data)


async def novus_parsing_all(page:Page):
    data = await read_json('novus.json')
    for item in data:
        await novus_parsing_one(page, item)