from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

from .services.flights import get_arrival_flights


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

app = FastAPI()

origins = [os.getenv("REACT_APP_HOST")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/flights/arrivals/{airport_code}")
async def get_flights_arrivals(airport_code: str, day: int = 1):
    if len(airport_code) != 3:
        raise HTTPException(status_code=400, detail="Airport code invalid!")

    airport_code = airport_code.upper()

    data = await get_arrival_flights(airport_code, day)

    return data


@app.get("/api/healthz")
def read_root():
    return {"Running": "OK"}


if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 3000))
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
