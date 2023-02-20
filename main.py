import argparse
from geopy.geocoders import Nominatim
from pandas import DataFrame


parser = argparse.ArgumentParser()
parser.add_argument('year')
parser.add_argument('latitude')
parser.add_argument('longtitude')
args = parser.parse_args()

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
            ind4 = film[2].find('(')
            if ind4 != -1:
                film[2] = ' '.join(film[2][:ind4].split(' ')[-3:])
            else:
                film[2] = ' '.join(film[2].split(' ')[-3:])
            films.append(film)
        data = DataFrame(films)
        data.columns = ['Name', 'Year', 'Location']
    return data

def find_coordinates(city: str):
    """
    Finds coordinates of the needed city
    """
    geolocator = Nominatim(user_agent="map")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude

def add_coordinates_to_df(df:DataFrame) -> DataFrame:
    """
    Finds coordinates of every location and saves them
    in a new column of DataFrame
    """
    df['Coordinates'] = [find_coordinates(city) for city in df['Location']]
    return df
