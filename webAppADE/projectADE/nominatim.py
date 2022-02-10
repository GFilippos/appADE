from geopy import Nominatim
from unidecode import unidecode

#get user data function




coord = (37.9739046, 23.6911461)
# get country
geolocator = Nominatim(user_agent='project')
x = geolocator.reverse(coord)
location = geolocator.geocode(x, exactly_one=True,language="english", namedetails=True, addressdetails=True)
# print(location.raw)
countryN = f"{location.raw['address']['country']}"

# get user location information
location = geolocator.reverse(coord)
user_info = location.address
