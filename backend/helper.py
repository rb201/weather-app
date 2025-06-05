from geopy.geocoders import Nominatim


def get_city_from_lon_lat(self):
    geolocater = Nominatim(user_agent="my-weather-app")

    location = geolocater.reverse(str(self.latitude) + "," + str(self.longitude))

    self.city = location.raw["address"]["city"].lower()
    self.state = location.raw["address"]["state"].lower()
    self.country = location.raw["address"]["country_code"].lower()


def get_coor_from_city_state(self, city: str, state: str):
    # geolocater = Nominatim(user_agent = 'my-weather-app')
    pass
