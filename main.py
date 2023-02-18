from geopy.geocoders import Nominatim
def find_coordinates(city: str):
    """
    Finds coordinates of the needed city
    """
    geolocator = Nominatim(user_agent="map")
    location = geolocator.geocode(city)
    return location.latitude, location.longitude
