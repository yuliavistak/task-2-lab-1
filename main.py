import argparse
from math import sin, cos, atan2, sqrt, pi
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
from pandas import DataFrame
import folium


parser = argparse.ArgumentParser()
parser.add_argument('year')
parser.add_argument('latitude')
parser.add_argument('longtitude')
parser.add_argument('path_to_dataset')
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
                film = [row[2:ind1 - 2], row[ind1:ind2 + 1], row[ind2 + 1:]]
            else:
                film = [row[2:ind1 - 2], row[ind1:ind2 + 1], row[ind3 + 1:]]
            ind4 = film[2].find('(')
            if ind4 != -1:
                film[2] = ', '.join(film[2][:ind4].split(', ')[-3:])
            else:
                film[2] = ', '.join(film[2].split(', ')[-3:])
            films.append(film)
        data = DataFrame(films)
        data.columns = ['Name', 'Year', 'Location']
    return data

def find_coordinates(city: str) -> tuple:
    """
    Finds coordinates of the needed city
    >>> find_coordinates('New York, USA')
    (40.7127281, -74.0060152)
    >>> find_coordinates('Львів')
    (49.841952, 24.0315921)
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
    coordinates = []
    for city in df['Location']:
        try:
            coordinates.append(find_coordinates(city))
        except GeocoderUnavailable:
            continue
    df['Coordinates'] = coordinates

    return df

def finding_distance_between_points(lat1, lat2, lon1, lon2):
    """
    Finds distance between two points in Earth by their
    coordinates
    >>> finding_distance_between_points(9.876, -4.879, 14.887, 77.987)
    7187015.417835812
    >>> finding_distance_between_points(98.768, 56.967, -6.886, 45.999)
    4328522.022720598
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
    distances = [finding_distance_between_points(float(lat1), float(i),\
         float(lon1), float(j)) for i, j in new_data['Coordinates']]
    new_data['Distance'] = distances
    new_data = new_data.sort_values(by = ['Distance'], ascending = True)[:10]
    return new_data

def create_map(data, lat1, lon1):
    """
    Creates a map with location tags
    """
    final_map = folium.Map(location = [lat1, lon1], zoom_start = 2)
    films_map_2 = folium.FeatureGroup(name="My location")
    label = folium.Marker(location = [lat1, lon1], popup = "You are here)")
    films_map_2.add_child(label)
    films_map_1 = folium.FeatureGroup(name="Films map")
    html = """<h4>Film information:</h4>
    Film name: {},<br>
    Year: {}
    """
    for crdnts in data['Coordinates']:
        ind = data.index[data['Coordinates'] == crdnts].tolist()[0]
        iframe = folium.IFrame(html=html.format(data['Name'].loc[ind], data['Year'].loc[ind]),
                          width=300,
                          height=100)
        films_map_1.add_child(folium.Marker(location=[crdnts[0], crdnts[1]],\
        popup=folium.Popup(iframe), icon=folium.Icon(), zoom_start = 5))

    final_map.add_child(films_map_1)
    final_map.add_child(films_map_2)
    final_map.add_child(folium.LayerControl())
    final_map.save('Map_of_nearest_locations.html')

if __name__ == '__main__':
    cont = read_file(args.path_to_dataset)
    data_with_distances = find_distance_between_locations(args.latitude, args.longtitude, \
        cont, args.year)
    create_map(data_with_distances, args.latitude, args.longtitude)

    import doctest
    print(doctest.testmod())
