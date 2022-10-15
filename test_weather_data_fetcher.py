import os
from unittest import mock

from weather_data_fetcher import fetch_location_coords, fetch_weather_data, get_api_key


class TestWeatherDataFetcher:
    def test_fetch_coords(self):
        coords_berlin = fetch_location_coords("Berlin")
        coords_difference = [sum(x) for x in zip(coords_berlin, (-52.520008, -13.404954))]
        assert sum(list(coords_difference)) < 0.01

    @mock.patch("weather_data_fetcher.fetch_new_data", autospec=True)
    def test_fetch_data(self, request_mock):
        request_mock.return_value = {
            "cod": "200",
            "message": 0,
            "cnt": 40,
            "list": [
                {
                    "dt": 1665824400,
                    "main": {
                        "temp": 12.95,
                        "feels_like": 12.76,
                        "temp_min": 12.95,
                        "temp_max": 13.93,
                        "pressure": 1000,
                        "sea_level": 1000,
                        "grnd_level": 1004,
                        "humidity": 94,
                        "temp_kf": -0.98,
                    },
                    "weather": [
                        {"id": 803, "main": "Clouds", "description": "broken clouds", "icon": "04d"}
                    ],
                    "clouds": {"all": 81},
                    "wind": {"speed": 1.55, "deg": 215, "gust": 3.1},
                    "visibility": 10000,
                    "pop": 0,
                    "sys": {"pod": "d"},
                    "dt_txt": "2022-10-15 09:00:00",
                },
            ],
            "city": {
                "id": 7576815,
                "name": "Alt-Kölln",
                "coord": {"lat": 52.517, "lon": 13.3889},
                "country": "DE",
                "population": 2000,
                "timezone": 7200,
                "sunrise": 1665811879,
                "sunset": 1665850372,
            },
        }
        fetch_weather_data(get_api_key(), (52.520008, 13.404954))
        assert request_mock.called
