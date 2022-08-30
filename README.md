# professional-python-exercises-1-weatherAPI

## Task

Exercieses complementing the Professional Python course on youtube - first exercise of communicating with an API

Exercise goals:

- Simple script as start
- Communicate with an external system
- Output things to console

- Fetch weather data
  - Weather history data last 3 days
  - Weather forecast for next 3 days
  - Extra: Display a temperature map (past or future)

## Function of the code in this repository

- The OpenWeatherMap API has been used in this repository (https://openweathermap.org/api, version 2.5 as this is free for use)
  - The api function used in this script is documented at: https://openweathermap.org/forecast5
- The free version will require an API key which is asked for at the beginning of the execution of the script
- Basically the Script asks the user to input a city for which to generate a forcast
- The forcast is set to be at least 3 days (25 timestamps in 3 hours intervals)
- Local caching is activated 
  - The json response from the api is saved as a file in the directory of the script
  - When executed again and less than one day has passed, the api is not triggered again but rather cached data is being read in
  - If the file is deleted the api is triggered anyway as loading from cache is impossible

## Usage

- Install the requirements with 
  - `pip install -r requirements.txt`
- Run the Python file: WeatherDataFetcher.py with `python WeatherDataFetcher.py`
- Input data as required
