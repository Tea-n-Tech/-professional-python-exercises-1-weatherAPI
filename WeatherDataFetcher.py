import os
import sys
import datetime
from typing import Tuple
from geopy.geocoders import Nominatim
import json
import requests


def fetch_weather_data(location_coords: Tuple[int, int], recent_data_available: bool):
    """
    Fetches data from the url if reload is active or no previous data was stored
    """

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/forecast?",
        params={
            "lat": location_coords[0],
            "lon": location_coords[1],
            "dt": 25,
            "units": "metric",
            "appid": api_key,
        },
    )

    file_path_json = os.getcwd() + "/data.json"
    if not os.path.exists(file_path_json) or not recent_data_available:
        data = response.json()
        with open(file_path_json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        with open(file_path_json, "r", encoding="utf-8") as f:
            data = json.loads(f.read())

    time_to_max_temp = {}
    time_to_min_temp = {}
    for _, values in enumerate(data["list"]):
        timestamp = datetime.datetime.utcfromtimestamp(values["dt"])
        time_to_max_temp[str(timestamp)] = values["main"]["temp_max"]
        time_to_min_temp[str(timestamp)] = values["main"]["temp_min"]

    print("Min Temperatures:")
    print(json.dumps(time_to_min_temp, indent=4))
    print("Max Temperatures:")
    print(json.dumps(time_to_max_temp, indent=4))


def fetch_location_coords(city: str) -> Tuple[int, int]:
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city)
    if location is None:
        print(
            f"Sorry, your input for the city ({city}) was not found, try again:",
            file=sys.stderr,
        )
        return fetch_location_coords(input("Where do you live?\n-->"))
    location_coords = (location.latitude, location.longitude)
    return location_coords


def get_api_key():

    if "TNT_EX1_OPENWEATHERMAP_API_KEY" not in os.environ:
        print(
            "No API Key found in your environment variables. \nPlease look at https://openweathermap.org/api for getting an API key and enter it in the following line:",
            file=sys.stderr,
        )
        os.environ["TNT_EX1_OPENWEATHERMAP_API_KEY"] = input(
            "Please enter your API Key now: \n-->"
        ).strip()
    api_key = os.environ["TNT_EX1_OPENWEATHERMAP_API_KEY"]
    if len(api_key) != 32:
        print(
            f"Wrong sized API Key inputted (correct length: 32), key found: {api_key}, \nplease look at https://openweathermap.org/api for getting an API key and enter it in the following line:",
            file=sys.stderr,
        )
        os.environ["TNT_EX1_OPENWEATHERMAP_API_KEY"] = input(
            "Please enter your API Key now:\n-->"
        ).strip()
        return get_api_key()
    return api_key


def recent_data_available():
    file_path_json = os.getcwd() + "/data.json"
    if not os.path.exists(file_path_json):
        return True
    else:
        with open(file_path_json, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            now_utc_in_s = datetime.datetime.now(datetime.timezone.utc).timestamp()
            oldest_utc_in_s = data["list"][0]["dt"]
            # Data is at least one day old
            if now_utc_in_s - oldest_utc_in_s > 86400:
                return False
    return True


if __name__ == "__main__":
    with open("api_key_open_weather_map.dat", "r", encoding="utf-8") as f:
        api_key = f.read()
    get_api_key()
    city = input("For which city should the forcast be generated for?\n-->")
    print(f"Generating forecast for the city: {city}")
    fetch_weather_data(fetch_location_coords(city), recent_data_available())
