import json
from fastapi import HTTPException
import httpx
import os
from dotenv import load_dotenv
from .utils import (
    get_flights_data,
    get_mock_data_file,
)


load_dotenv()

USE_MOCK_DATA = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
API_KEY = os.getenv("API_KEY")


async def get_arrival_flights_from_external_api(
    airport_code: str, day: int = 1
) -> list:
    # Try to use mock data first if available for demo purposes
    mock_file = get_mock_data_file(airport_code)
    try:
        with open(mock_file, "r") as file:
            print(f"Found mock data for {airport_code}, using it instead of API")
            data_str = file.read()
            return get_flights_data(airport_code, day, data_str)
    except FileNotFoundError:
        print(f"No mock data for {airport_code}, falling back to API")
        pass

    url = f"https://api.flightapi.io/compschedule/{API_KEY}?mode=arrivals&iata={airport_code}&day={day}"
    print(url)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30)
            response.raise_for_status()
            # Convert response data to string for caching
            data_str = json.dumps(response.json())
            return get_flights_data(airport_code, day, data_str)
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"External API request failed: {str(e)}"
            )


async def get_arrival_flights_from_mock_data(
    airport_code: str = "SIN", day: int = 1
) -> list:
    try:
        mock_data_file = get_mock_data_file(airport_code)
        with open(mock_data_file, "r") as file:
            data_str = file.read()
            return get_flights_data(airport_code, day, data_str)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Mock data file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error decoding mock data file")


async def get_arrival_flights(airport_code: str, day: int) -> list:
    if USE_MOCK_DATA:
        print("Using mock data, simulating external API call...")
        return await get_arrival_flights_from_mock_data(airport_code)
    else:
        print("Fetching data from external API...")
        return await get_arrival_flights_from_external_api(airport_code, day)
