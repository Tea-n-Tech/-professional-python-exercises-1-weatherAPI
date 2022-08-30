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

- The OpenWeatherMap API has been used in this repository
- The free version will require an API key which is asked for at the beginning
- Basically the Script asks the user to input a city for which to generate a forcast
- The forcast is set to be at least 3 days (25 timestamps in 3 hours intervals)

## Usage

- Install the requirements with 
  - `pip install -r requirements.txt`
- Run the Python file: WeatherDataFetcher.py with `python WeatherDataFetcher.py`
- Input data as required
