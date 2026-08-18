import asyncio
import json,os
from pathlib import Path

base_dir = Path(__file__).resolve().parent
folder_path = base_dir / 'urls_db'

async def read_json(name:str):
    if(os.path.exists(folder_path / name)):
        with open(folder_path/name, 'r', encoding='utf-8') as r:
            read_data = json.load(r)
            return read_data
    else:
        return []

async def add_json(first_data:list, json_name:str):
    second_data:list = await read_json(json_name)
    data = list(set(first_data + second_data))
    if(os.path.exists(folder_path)):
        with(open(folder_path / json_name, 'w', encoding='utf-8')) as w:
            json.dump(data, w)
    else:
        os.mkdir(folder_path)