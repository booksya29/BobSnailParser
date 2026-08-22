import asyncio
import os
import sys
import time
from pathlib import Path
import pandas

if getattr(sys, "frozen", False):
    file_name = Path(sys.executable).resolve().parent / "data.xlsx"
else:
    file_name = Path(__file__).resolve().parent.parent / "data.xlsx"

_excel_lock = asyncio.Lock()


async def add_to_excel(data: dict):
    if not data or not isinstance(data, dict):
        return
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
                break
            except PermissionError:
                await asyncio.sleep(1)
            except Exception as error:
                print(f"Error saving to Excel: {error}")
                break
