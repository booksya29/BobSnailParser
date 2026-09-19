import asyncio
import os
import sys
import time
from pathlib import Path
import pandas
from patchright.async_api import async_playwright

if getattr(sys, "frozen", False):
    file_name = Path(sys.executable).resolve().parent / "Моніторинг.xlsx"
else:
    file_name = Path(__file__).resolve().parent.parent / "Моніторинг.xlsx"
if getattr(sys, "frozen", False):
    file_name_new = Path(sys.executable).resolve().parent / "Моніторинг АТБ.xlsx"
else:
    file_name_new = Path(__file__).resolve().parent.parent / "Моніторинг АТБ.xlsx"
_excel_lock = asyncio.Lock()

async def add_to_excel_new(data: dict):
    data['time'] = time.strftime("%d.%m.%Y", time.localtime())
    if not data or not isinstance(data, dict):
        return
    shop = data.get("shop", "Невідомий магазин")
    url = data.get("url", "")
    if data.get("name", "-") == "-":
        print(f"[{shop}] Не вдалося знайти назву товару: {url}")
    if data.get("price", "-") == "-":
        print(f"[{shop}] Не вдалося знайти ціну основного товару: {url}")
    else:
        print(f"[{shop}] Знайдено ціну: {data['price']}; акційна: {data.get('sale_price', '-')}")
    global file_name_new
    async with _excel_lock:
        for attempt in range(5):
            try:
                new_data = pandas.DataFrame([data])
                if os.path.exists(file_name_new):
                    try:
                        old_data = pandas.read_excel(file_name_new)
                        combined_data = pandas.concat([old_data, new_data], ignore_index=True)
                    except Exception:
                        combined_data = new_data
                    combined_data.to_excel(file_name_new, index=False)
                else:
                    new_data.to_excel(file_name_new, index=False)
                print(f"[{shop}] Дані записано у {file_name_new.name}.")
                break
            except PermissionError:
                print(f"[{shop}] Не можу записати {file_name_new.name}: закрийте файл Excel і спробуйте ще раз.")
                await asyncio.sleep(1)
            except Exception as error:
                print(f"Error saving to Excel: {error}")
                break

async def add_to_excel(data: dict):
    data['time'] = time.strftime("%d.%m.%Y", time.localtime())
    if not data or not isinstance(data, dict):
        return
    shop = data.get("shop", "Невідомий магазин")
    url = data.get("url", "")
    if data.get("name", "-") == "-":
        print(f"[{shop}] Не вдалося знайти назву товару: {url}")
    if data.get("price", "-") == "-":
        print(f"[{shop}] Не вдалося знайти ціну основного товару: {url}")
    else:
        print(f"[{shop}] Знайдено ціну: {data['price']}; акційна: {data.get('sale_price', '-')}")
    global file_name
    async with _excel_lock:
        for attempt in range(5):
            try:
                new_data = pandas.DataFrame([data])
                if os.path.exists(file_name):
                    try:
                        old_data = pandas.read_excel(file_name)
                        combined_data = pandas.concat([old_data, new_data], ignore_index=True)
                    except Exception:
                        combined_data = new_data
                    combined_data.to_excel(file_name, index=False)
                else:
                    new_data.to_excel(file_name, index=False)
                print(f"[{shop}] Дані записано у {file_name.name}.")
                break
            except PermissionError:
                print(f"[{shop}] Не можу записати {file_name.name}: закрийте файл Excel і спробуйте ще раз.")
                await asyncio.sleep(1)
            except Exception as error:
                print(f"Error saving to Excel: {error}")
                break