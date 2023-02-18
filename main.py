import pandas as pd
def read_file(file_path:str):
    """
    Reads information from file and represents it in DataFrame
    """
    with open(file_path, 'r', encoding = 'utf-8') as file:
        content = file.read().replace('\t', '').strip().split('\n')[14:]
        films = []
        for row in content:
            ind1 = row.find('(')
            ind2 = row.find(')')
            ind3 = row.find('}')
            if ind3 == -1:
                films.append((row[:ind1 - 1], row[ind1:ind2 + 1], row[ind2 + 1:]))
            else:
                films.append((row[:ind1 - 1], row[ind1:ind2 + 1], row[ind3 + 1:]))
        data = pd.DataFrame(films)
        data.columns = ['Name', 'Year', 'Location']
    return data
