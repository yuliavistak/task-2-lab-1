import pandas as pd
def read_file(file_path:str):
    with open(file_path, 'r', encoding = 'utf-8') as file:
        data = file.read().strip('').split('\n')[14:]
    return data
