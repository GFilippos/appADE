from geopy import Nominatim
from unidecode import unidecode
import json



#get user data function
def reverseGeo(position):
    print(type(position))
    coords = (37.9789595, 23.6561609)
    # parse position into coords
    # coords = (position[0], position[1])
    # get country
    geolocator = Nominatim(user_agent='project')
    x = geolocator.reverse(coords)
    location = geolocator.geocode(x, exactly_one=True,language="english", namedetails=True, addressdetails=True)
    # print(location.raw)
    countryN = f"{location.raw['address']['country']}"
    # get user location information
    location = geolocator.reverse(coords)
    user_info = location.address
    return countryN, user_info