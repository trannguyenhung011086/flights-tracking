# Function to fetch data from the external API
from collections import defaultdict
import json
from fastapi import HTTPException
import httpx
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))


USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
MOCK_DATA_FILE = os.path.join(os.path.dirname(__file__), "sample.json")

API_KEY = os.getenv("API_KEY")


# the free tier has 20 credits for an account so we need to use mock data for this demo
async def get_arrival_flights_from_external_api(
    airport_code: str, day: int = 1
) -> list:

    url = f"https://api.flightapi.io/compschedule/{API_KEY}?mode=arrivals&iata={airport_code}&day={day}"
    print(url)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"External API request failed: {str(e)}"
            )


async def get_arrival_flights_from_mock_data(airport_code: str = "SIN") -> list:
    try:
        with open(MOCK_DATA_FILE, "r") as file:
            mock_data = json.load(file)

        aggregated_flights = []

        for entry in mock_data:
            try:
                arrivals_data = entry["airport"]["pluginData"]["schedule"]["arrivals"][
                    "data"
                ]
                aggregated_flights.extend(arrivals_data)
            except KeyError as e:
                raise HTTPException(
                    status_code=500, detail=f"Error in mock data structure: {e}"
                )
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

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Mock data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding mock data file")


async def get_arrival_flights(airport_code: str, day: int) -> list:
    if USE_MOCK_DATA:
        print("Using mock data")
        return await get_arrival_flights_from_mock_data(airport_code)
    else:
        print("Fetching data from external API")
        return await get_arrival_flights_from_external_api(airport_code, day)
