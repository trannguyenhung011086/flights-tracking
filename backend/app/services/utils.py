from collections import defaultdict
from functools import lru_cache
import json
import os


MOCK_DATA_DIR = os.path.join(os.path.dirname(__file__), "mocked_data")
DEFAULT_AIRPORT = "SIN"


def get_mock_data_file(airport_code: str) -> str:
    file_path = os.path.join(MOCK_DATA_DIR, f"{airport_code}.json")
    if os.path.exists(file_path):
        return file_path
    return os.path.join(MOCK_DATA_DIR, f"{DEFAULT_AIRPORT}.json")


def parse_flights_arrivals(airport_code: str, data: list) -> list:
    aggregated_flights = []

    for entry in data:
        try:
            arrivals_data = entry["airport"]["pluginData"]["schedule"]["arrivals"][
                "data"
            ]
            aggregated_flights.extend(arrivals_data)
        except KeyError as e:
            raise HTTPException(status_code=500, detail=f"Error in data structure: {e}")
    print(f"Total flights to {airport_code}:", len(aggregated_flights))

    country_flight_count = defaultdict(int)

    for flight in aggregated_flights:
        try:
            country = flight["flight"]["airport"]["origin"]["position"]["country"][
                "name"
            ]
            country_flight_count[country] += 1
        except KeyError as e:
            continue

    country_flight_list = [
        {"country": country, "flights": count}
        for country, count in country_flight_count.items()
    ]

    print("The first country:", country_flight_list[0])

    return country_flight_list


@lru_cache(maxsize=100)
def _get_flights_data_cached(airport_code: str, day: int, data_str: str) -> list:
    data = json.loads(data_str)
    return parse_flights_arrivals(airport_code, data)


def get_flights_data(airport_code: str, day: int, data_str: str) -> list:
    result = _get_flights_data_cached(airport_code, day, data_str)
    cache_info = _get_flights_data_cached.cache_info()
    if cache_info.hits > cache_info.misses:
        print(f"Cache hit for airport {airport_code}! Current stats: {cache_info}")
    else:
        print(f"Cache miss for airport {airport_code}. Current stats: {cache_info}")
    return result
