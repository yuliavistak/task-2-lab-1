import argparse
from math import sin, cos, atan2, sqrt, pi
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
                film[2] = ', '.join(film[2][:ind4].split(', ')[-3:])
            else:
                film[2] = ', '.join(film[2].split(', ')[-3:])
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

def add_coordinates_to_df(df:DataFrame, year) -> DataFrame:
    """
    Finds coordinates of every location and saves them
    in a new column of DataFrame
    """
    df = df.loc[df['Year'] == f'({year})']
    df['Coordinates'] = [find_coordinates(city) for city in df['Location']]

    return df

def finding_distance_between_points(lat1, lat2, lon1, lon2):
    """
    Finds distance between two points in Earth by their
    coordinates
    """
    radius = 6.3781 * 10**6 #approximate earth's radius
    fi1 = lat1 * pi/180
    fi2 = lat2 * pi/180
    dfi = (lat2-lat1) * pi/180
    dlambda = (lon2-lon1) * pi/180

    const1 = (sin(dfi / 2) ** 2) + cos(fi1) * cos(fi2) * (sin(dlambda / 2) ** 2)
    const2 = 2 * atan2(sqrt(const1), sqrt(1 - const1))

    return radius * const2

def find_distance_between_locations(lat1, lon1, data: DataFrame, year):
    """
    Finds distance between two positions and returns
    possible places for the label
    """
    new_data = add_coordinates_to_df(data, year)
    new_data['Distance'] = [finding_distance_between_points(float(lat1), float(i),\
         float(lon1), float(j)) for i, j in new_data['Coordinates']]
    new_data = new_data.sort_values(by = ['Distance'], ascending = True)[:10]
    return new_data
