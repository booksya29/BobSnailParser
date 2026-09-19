# Дніпро Fozzy (Дніпро) https://fozzyshop.ua/ Дніпро
import sys
import threading
import tkinter as tk
from tkinter import messagebox
from PySide6.QtWidgets import QMessageBox
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import asyncio
import re
from patchright.async_api import async_playwright, TimeoutError, Page
from excel_add import add_to_excel_new
from json_manager import read_json


login_done = False
login_event = threading.Event()


def show_message():
    global login_done

    root = tk.Tk()
    root.withdraw()

    root.attributes("-topmost", True)

    messagebox.showinfo(
        "Авторизація",
        "Пройди авторизацію та натисни OK",
        parent=root
    )

    login_done = True
    login_event.set()

    root.destroy()


async def check_registration(page: Page) -> bool:
    global login_done
    global login_event
    await page.wait_for_load_state('domcontentloaded')
    try:
        user_name = (
            await page.locator(
                'span[class="header-user-login"]'
            ).text_content(timeout=2000)
        ).strip()
        print('Не зареєстрований ', user_name)

        login_event.clear()

        threading.Thread(
            target=show_message,
            daemon=True
        ).start()

        return False

    except TimeoutError:
        print('Зареєстрований')
        return True


def clean_p(v):
    if not v or v == '-' or v == 0 or v == '0':
        return '-'
    s = re.sub(r'\s+', '', str(v).replace('\xa0', ' '))
    m = re.search(r'\d+[\,\.]\d{2}|\d+', s)
    return m.group(0).replace(',', '.') if m else str(v).strip()


def clean_prod(v):
    if not v or v == '-' or v == 'NULL':
        return '-'
    cleaned = re.sub(
        r'^(Бренд|ТМ|Виробник|Торгова марка)\s*:?\s*',
        '',
        str(v),
        flags=re.I
    ).strip()
    return cleaned if len(cleaned) <= 40 else '-'

async def select_addr(page: Page):
    addr_name = await page.locator('span[class="line line-address"]').nth(1).text_content()
    if "Київ, Заболотного" in addr_name:
        return True
    await page.locator('button[class*="btn btn-delivery"]').first.click()
    await page.locator('div[class*="checkin_selector_block self_pickup"]').click()
    try:
        await page.locator('div[id="checkin_content_addresses_content"]').locator('div[class*="checkin_address_block"]', has_text='Київ, Заболотного').text_content(timeout=2000)
        print('Знайшов в переліку')
    except:
        print('Не знайшов в переліку')
        try:
            await page.locator('div[class="checkin_content_addresses_header_add"]').click(timeout=2000)
        except TimeoutError:
            await page.locator('div[class*="checkin_content_addresses_body_add"]').click()
        await page.locator('div[class="add_address_list js-pickup-address-list"]').get_by_text('Київ, Заболотного').click()
        await page.locator('button[class="add_address_button"]').click()
        await page.locator('div[id="timeslots_button_panel"]').click()
        return True
    
    await page.locator('div[class*="checkin_address_block"]', has_text='Київ, Заболотного').click()
    await page.locator('div[id="checkin_content_addresses_button_block"]', has_text='Продовжити').click()
    


async def check_in_stock(page: Page) -> bool:
    try:
        res = await page.evaluate('''() => {
            const text = (document.querySelector('main, div.product_header_container, div.primary_block')?.innerText || '').toLowerCase();
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
                if (text.includes(m)) return false;
            }
            const outEl = document.querySelector('[data-marker*="Out of Stock"], [data-marker*="outOfStock"], .out-of-stock, [class*="not-available"]');
            if (outEl) return false;
            return true;
        }''')
        return bool(res)
    except Exception:
        return True


async def fozzy_parsing_one(page: Page, url: str):
    global login_done

    for _ in range(3):
        try:
            await page.goto(
                url,
                wait_until='load',
                timeout=30000
            )
            await page.wait_for_selector('h1', timeout=15000)
            break
        except TimeoutError:
            print(f"Can't load {url}")
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
        await asyncio.sleep(3)
    else:
        return

    check_registration_bool = await check_registration(page)

    if check_registration_bool == False:
        while not login_event.is_set():
            await asyncio.sleep(0.1)

        check_registration_bool = await check_registration(page)
    await select_addr(page)
    await page.goto(url)
    await page.wait_for_load_state('domcontentloaded')
    product_name = '-'
    for _ in range(30):
        try:
            h1 = await page.locator(
                'h1, div[class*="product_name"]'
            ).first.text_content(timeout=500)

            if h1 and h1.strip() and len(h1.strip()) > 3:
                product_name = h1.strip()
                break

            if '404' in h1:
                return False
        except Exception:
            pass

        await asyncio.sleep(0.2)

    in_stock = await check_in_stock(page)

    if not in_stock:
        print(
            f"[Фоззі] Товар відсутній в наявності: "
            f"{url} - пропуск."
        )
        return

    if product_name == '-':
        try:
            t = await page.title()
            if t:
                product_name = re.split(
                    r' - | \| | купити',
                    t
                )[0].strip()
        except Exception:
            product_name = '-'

    container = page.locator(
        'div.product_header_container, '
        'div[class*="product-container"], '
        'div.primary_block, main'
    ).first

    price_wrap = container.locator(
        'div.main_price_block, '
        'div.product-prices, '
        'div.current-price'
    ).first

    old_price = '-'
    regular_price = '-'

    try:
        old_el = price_wrap.locator(
            'span.old_price, span[class*="old_price"]'
        )

        reg_el = price_wrap.locator(
            'span.regular_price, span.price, div.current-price span'
        )

        has_old = await old_el.count() > 0

        old_price = (
            await old_el.first.text_content(timeout=1000)
            if has_old else '-'
        )

        regular_price = (
            await reg_el.first.text_content(timeout=1000)
            if await reg_el.count() > 0 else '-'
        )

        if has_old and old_price != '-':
            price = old_price
            sale_price = regular_price
        else:
            price = regular_price
            sale_price = '-'

    except Exception:
        price = '-'
        sale_price = '-'

    producer = '-'

    try:
        raw_producer = await container.locator(
            'div.product_characteristics_item',
            has_text='Бренд'
        ).first.locator(
            'a, span'
        ).first.text_content(timeout=1000)

        producer = raw_producer.strip() if raw_producer else '-'

    except Exception:
        producer = '-'

    id = '-'

    try:
        id_not_sep = await page.locator(
            'div[class="reference_block"]'
        ).locator(
            'span[class="product_reference"]'
        ).text_content()

        id = (id_not_sep.split(':'))[1].strip()

    except TimeoutError:
        id = '-'

    data = {
        'shop': 'Fozzy',
        'name': product_name,
        'price': clean_p(price),
        'sale_price': clean_p(sale_price),
        'producer': clean_prod(producer),
        'url': page.url,
        'id': id,
        'Адреса': 'Київ. Заболотного 37'
    }

    await add_to_excel_new(data)

    print(data)


async def fozzy_parsing_all(page: Page, on_progress=None):
    data = await read_json('kyiv_fozzy_zabolotnogo.json')

    if not data:
        if on_progress:
            on_progress(100)
        return

    total = len(data)

    for i, item in enumerate(data, start=1):
        try:
            await fozzy_parsing_one(page, item)

        except Exception as e:
            print(
                f"Error parsing Fozzy item {item}: {e}"
            )

        if on_progress:
            on_progress(
                int((i / total) * 100)
            )

        await asyncio.sleep(1)


async def test():
    async with async_playwright() as pw:
        bw = await pw.chromium.launch(
            headless=False
        )
        context = await bw.new_context(storage_state='storage_state.json')
        page = await context.new_page()

        urls = [
            'https://fozzyshop.ua/kvas/923493-kvas-kvas-taras-khlibnyi-z-b.html',
            'https://fozzyshop.ua/vitchyznyane-pyvo/921564-pyvo-lvivske-1715-svitle.html'
        ]

        for i in urls:
            await fozzy_parsing_one(page, i)
            await asyncio.sleep(1)
        await context.storage_state(path='storage_state.json')

if __name__ == '__main__':
    asyncio.run(test())