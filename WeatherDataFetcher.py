import os
import datetime
from typing import Tuple
from geopy.geocoders import Nominatim
import urllib.request, json


class Weather_Forecast_Fetcher:
    """
    This class provides 3 days of forecast from an open API for a given location
    api_key_open_weather_map.dat should contain the api key

    Parameters:
    ----------
    city : stry
      City for which the forcast will be given
    location_coords : Tuple
      Latitude and Longitude Coordinates of the location of interest (self.city)
    api_key : str
      API Key used for OpenWeatherMap


    """

    location_coords: Tuple = (0, 0)
    api_key: str = ""

    def __init__(self, api_key: str):
        """
        Initializes the class
        """
        location_coords_fetcher = Location_Coords_Fetcher()
        self.location_coords = location_coords_fetcher.location_coords
        self.city = location_coords_fetcher.city
        self.api_key: str = api_key

    def fetch_weather_data(self, reload=False):
        """
        fetches data from the url if reload is active or no previous data was stored
        """
        request = (
            f"https://api.openweathermap.org/data/2.5/"
            + f"forecast?lat={self.location_coords[0]}&lon={self.location_coords[1]}"
            + f"&dt=25&units=metric"
            + f"&appid={self.api_key}"
        )

        file_path_json = os.getcwd() + "/data.json"
        if reload or not os.path.exists(file_path_json):
            with urllib.request.urlopen(request) as url:
                data = json.loads(url.read().decode())
                with open(file_path_json, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            with open(file_path_json, "r", encoding="utf-8") as f:
                data = json.loads(f.read())

        for _, values in enumerate(data["list"]):
            timestamp_utc = values["dt"]
            timestamp = datetime.datetime.utcfromtimestamp(timestamp_utc)
            temp_min = values["main"]["temp_min"]
            temp_max = values["main"]["temp_max"]
            print(
                f"On:{timestamp}, the min Temp is: {temp_min} and the max Temp is {temp_max}"
            )


class Location_Coords_Fetcher:
    """
    Class for getting location coordinates (long and lat) for a given city
    Parameters
    ---------
    city : str
      Name of the city for the coordinates
    location_coords : Tuple
      (lat, long) for the self.city
    """

    def __init__(self):
        self.location_coords = self.fetch_location_coords()

    def fetch_location_coords(self) -> Tuple:
        # ask user for city
        self.city = input("Where do you live?\n-->")
        # city = "Berlin"
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(self.city)
        if location is None:
            print(
                f"Sorry, your input for the city ({self.city}) was not found, try again:"
            )
            return self.fetch_location_coords()
        location_coords = (location.latitude, location.longitude)
        return location_coords


if __name__ == "__main__":
    with open("api_key_open_weather_map.dat", "r", encoding="utf-8") as f:
        api_key = f.read()
    forcaster = Weather_Forecast_Fetcher(api_key)
    forcaster.fetch_weather_data(reload=True)
