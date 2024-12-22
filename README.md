# flights-tracking

Learning app to use FastAPI and Python

# Overview

The user will enter a 3-character airport code, such as SIN for Singapore Changi Airport.
The tool will query the FlightAPI.io API and display a table with two columns:

- Country – The country flights are arriving from.
- Number of Flights – The number of flights originating from that country and arriving at the entered airport.

# Structure

```
├── backend -> use FastAPI framework to build API endpoints
│   └── app
└── frontend -> use React to host the form
    ├── public
    └── src
```

# How to run on local

## Backend

Backend is built with Python3 and FastAPI framework to establish the main endpoint `/api/flights/arrivals/{airport_code}` for front end to call to.
_Notes: should activate virtual environment when developing (see https://fastapi.tiangolo.com/virtual-environments/)_

Steps:

- Run `pip install -r requirements.txt`
- Copy `.env.example` to `.env` to use
- Run `uvicorn app.main:app --port=3000 --reload` or `python3 -m app.main` to start the server

Another note is FlightAPI.io charges credits for every call so for demo purpose, the backend will use mock data from `/app/services/sample.json` to return the result.
In reality, there should be a caching layer (like Redis) to cache data then store to database (like Postgres) so the backend can fetch from there to serve.

## Frontend

Frontend is created with create-react-app and uses `react-query` to query API endpoints from the backend.
_Notes: currently react-query does not work with React 19 yet, so need to downgrade to React 18._

Steps:

- Run `npm install`
- Copy `.env.example` to `.env` to use
- Run `npm run start`

# How to deploy

For demo purpose, both backend and frontend parts use render.com platform to host on FREE tier.

- Backend uses `dockerfile` to containerize the application.
- Frontend is built and exposed as a static site.
- The `render.yaml` defines backend as a web service and frontend as a static site to deploy.
