import os
import datetime
from typing import Tuple, Final
from geopy.geocoders import Nominatim
import urllib.request, json


class Weather_Forecast_Fetcher:
    """
    This class provides 3 days of forecast from an open API for a given location
    api_key_open_weather_map.dat should contain the api key

    Parameters:
    ----------
    location_coords : Tuple
      Latitude and Longitude Coordinates of the location of interest
    api_key : str
      API Key used for OpenWeatherMap


    """

    location_coords: Tuple = (0, 0)
    api_key: str = ""

    def __init__(self, location_coords: Tuple, api_key: str):
        """
        Initializes the class
        """
        self.location_coords = location_coords
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
        print(request)
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


if __name__ == "__main__":
    with open("api_key_open_weather_map.dat", "r", encoding="utf-8") as f:
        api_key = f.read()

    # ask user for city
    # city: str = input("Where do you live?\n-->")
    city = "Berlin"
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    location_coords = (location.latitude, location.longitude)
    print(location_coords)
    forcaster = Weather_Forecast_Fetcher(location_coords, api_key)
    forcaster.fetch_weather_data(reload=False)
