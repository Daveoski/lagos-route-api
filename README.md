# The Lagos Route Window

A read-only FastAPI service for querying Lagos routes and buses.

# Features
it will 
- Get route and bus counts
- Get complete route details
- Get route stops
- Search routes by destination
- Filter routes by maximum fare
- Find buses by plate
- Filter buses by bus type
- Get buses serving a route
- Declarative validation using FastAPI Path and Query
- Automatic API documentation with Swagger UI

## Project Structure

```text
lagos-route-window/
│
├── .gitignore
├── data.py
├── lagos_routes.json
├── main.py
├── README.md
└── requirements.txt