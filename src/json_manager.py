import asyncio
import json
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent
folder_path = base_dir / 'urls_db'

async def read_json(name: str) -> list:
    file_target = folder_path / name
    if os.path.exists(file_target):
        try:
            with open(file_target, 'r', encoding='utf-8') as r:
                read_data = json.load(r)
                if isinstance(read_data, list):
                    return read_data
                return []
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading {file_target}: {e}")
            return []
    else:
        return []

async def add_json(first_data: list, json_name: str):
    if not isinstance(first_data, list):
        first_data = [first_data] if first_data else []
    second_data: list = await read_json(json_name)
    data = list(set(first_data + second_data))
    
    os.makedirs(folder_path, exist_ok=True)
    try:
        with open(folder_path / json_name, 'w', encoding='utf-8') as w:
            json.dump(data, w, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"Error saving {json_name}: {e}")