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
                film = [row[:ind1 - 1], row[ind1:ind2 + 1], row[ind2 + 1:]]
            else:
                film = [row[:ind1 - 1], row[ind1:ind2 + 1], row[ind3 + 1:]]
            if '(' in film[2]:
                ind4 = film[2].find('(')
                film[2] = film[2][:ind4]
            films.append(film)
        data = DataFrame(films)
        data.columns = ['Name', 'Year', 'Location']
    return data
