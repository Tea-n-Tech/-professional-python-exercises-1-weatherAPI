import os
import sys
import datetime
from typing import Tuple
import json
import requests
import dotenv
from geopy.geocoders import Nominatim


def fetch_weather_data(api_key: str, location_coords: Tuple[int, int]) -> None:
    """
    Fetches weather data for 25 timepoints from the url if no recent data is available
    Stores the data in the folder where it is executed for future use.

    Parameters:
    ---------
    location_coords : Tuple[int, int]
      (lat,long) coordinates for the city entered
    recent_data_available : bool
      if true, use cached values (load from file)
      if false, reload from url (requests)

    """

    # Check if fetch_data_from_url is necessary
    file_path_json = os.getcwd() + "/data.json"
    fetch_data_from_url = False
    if not os.path.exists(file_path_json):
        fetch_data_from_url = True
    else:
        with open(file_path_json, "r", encoding="utf-8") as file:
            data = json.loads(file.read())
        now_utc_in_s = datetime.datetime.now(datetime.timezone.utc).timestamp()
        oldest_utc_in_s = data["list"][0]["dt"]
        # Data is more than day old - fetch_data_from_url required
        seconds_in_one_day = 86400
        if now_utc_in_s - oldest_utc_in_s > seconds_in_one_day:
            fetch_data_from_url = True
        # Different location is requested - fetch_data_from_url required
        lat = data["city"]["coord"]["lat"]
        lon = data["city"]["coord"]["lon"]
        threshold = 0.001
        if abs(lat - location_coords[0]) > threshold:
            fetch_data_from_url = True
        if abs(lon - location_coords[1]) > threshold:
            fetch_data_from_url = True

    if not os.path.exists(file_path_json) or fetch_data_from_url:
        print("Getting new data from URL", file=sys.stderr)
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                "lat": location_coords[0],
                "lon": location_coords[1],
                "dt": 25,
                "units": "metric",
                "appid": api_key,
            },
            timeout=15,
        )
        data = response.json()
        with open(file_path_json, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    else:
        print("Getting new data local file", file=sys.stderr)
        with open(file_path_json, "r", encoding="utf-8") as file:
            data = json.loads(file.read())

    time_to_max_temp = {}
    time_to_min_temp = {}
    for _, values in enumerate(data["list"]):
        timestamp = datetime.datetime.utcfromtimestamp(values["dt"])
        time_to_max_temp[str(timestamp)] = values["main"]["temp_max"]
        time_to_min_temp[str(timestamp)] = values["main"]["temp_min"]

    output = {}
    print("Temperatures: ", file=sys.stderr)
    output["max_temperatures"] = time_to_max_temp
    output["min_temperatures"] = time_to_min_temp
    print(output)


def fetch_location_coords(city: str) -> Tuple[int, int]:
    """
    Gets the (lat, long) coordinates of a city name. If the city cannot be found
    (e.g. invalid user input) the user is asked to input it again.

    Parameters:
    ----------
    city : str
      Name of the city to get the coordinates for

    Returns:
    ----------
    location_coords : Tuple[int,int]
      (lat,long) coordinates for the city entered
    """

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


def get_api_key() -> str:
    """
    Checks, if API Key is set as an environment variable. If not, the user is
    asked to input it in the console. Length checks enabled for the API key. If
    key has non-valid length (!=32) the user is asked again to enter a valid key.
    The key is saved into a local .env file.

    Returns:
    api_key : str
      API Key for the Open Weather Map

    """

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    if "TNT_EX1_OPENWEATHERMAP_API_KEY" not in os.environ:
        print(
            "No API Key found in your environment variables. \nPlease look at "
            "https://openweathermap.org/api for getting an API key and enter it "
            "in the following line:",
            file=sys.stderr,
        )
        os.environ["TNT_EX1_OPENWEATHERMAP_API_KEY"] = input(
            "Please enter your API Key now: \n-->"
        ).strip()
    api_key = os.environ["TNT_EX1_OPENWEATHERMAP_API_KEY"]
    if len(api_key) != 32:
        print(
            f"Wrong sized API Key inputted (correct length: 32), key found: {api_key},"
            "\nplease look at https://openweathermap.org/api for getting an API key and"
            "enter it in the following line:",
            file=sys.stderr,
        )
        os.environ["TNT_EX1_OPENWEATHERMAP_API_KEY"] = input(
            "Please enter your API Key now:\n-->"
        ).strip()
        return get_api_key()

    dotenv.set_key(
        dotenv_file, "TNT_EX1_OPENWEATHERMAP_API_KEY", api_key
    )  # save the API key to .env file
    return api_key


def main() -> None:
    """
    Main method which fetches first the API key for open weather map.
    Aks for city name input and outputs json format for a forcast of
    25 timestamps with at least 3hours apart.
    """
    city = input("For which city should the forcast be generated for?\n-->")
    print(f"Generating forecast for the city: {city}", file=sys.stderr)
    api_key = get_api_key()
    location_coords = fetch_location_coords(city)
    fetch_weather_data(api_key, location_coords)


if __name__ == "__main__":
    main()
