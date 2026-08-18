import os, pandas

file_name = 'data.xlsx'

async def add_to_excel(data:dict):
    global file_name
    new_data = pandas.DataFrame([data])
    if os.path.exists(file_name):
        old_data = pandas.read_excel(file_name)
        combined_data = pandas.concat([old_data, new_data], ignore_index=True)
        combined_data.to_excel(file_name, index=False)
    else:
        new_data.to_excel(file_name)
