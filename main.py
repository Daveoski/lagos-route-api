from typing import Annotated, Any, Literal
from fastapi import FastAPI, HTTPException, Path, Query
from data import DATA

app: FastAPI = FastAPI(
    title="Lagos Route Window",
    description="A FastAPI service that returns the route window for a given Lagos station and buses.",
    version="1.0.0",
)


RouteNumber = Annotated[
    int,
    Path(
        ge=1,
        le=200,
        title="Route Number",
        description="Lagos route number must be between 1 and 200.",
    ),
]


plate = Annotated[
    str,
    Path(
        pattern=r"^[A-Z]{3}-\d{3}[A-Z]{2}$",
        title="Plate Number",
        description="Plate number must be in three capital letters, a dash, three digits, and two capital letters.",
    ),
]
BusType = Annotated[
    Literal["brt", "danfo", "keke",],
    Path(
        title="Bus Type",
        description="the union operates brt, danfo, and keke buses.",   
    ),
    ]
    
    
def find_route(route_number: int,) -> dict[str, Any] | None:
    #  finds a route by its route number
    return next(
    (
        route
        for route in DATA["routes"]
        if route["route_number"] == route_number
        
    )
    , None
)
    
    
@app.get("/")
def home() -> dict[str, Any]:
    """returns a welcome message and current fleet count"""
    return {
        "message": "Welcome to the Lagos Route Window API!",
        "documentation": len(DATA["routes"]),
        "buses": len(DATA["buses"]),
    }
    
    
    
@app.get("/route/{route_number}/stops")
def get_route_stops(
    route_number: RouteNumber,
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=10,
            title="Number of stops to show",
            description="Show between 1 and 10 stops, default to 5.",
        ),
    ] = 5,
    skip: Annotated[
        int,
        Query(
            ge=0,
            title="Number of stops to skip",
            description="Skip zero or more stops before returning results.",
        ),
    ] = 0,
) -> dict[str, Any]:
    """Return a limited, optionally skipped list of stops for one route."""
    route: dict[str, Any] | None = find_route(route_number)
    if route is None:
        raise HTTPException(status_code=404, detail="Route not found")

    stops: list[str] = route["stops"]
    selected_stops: list[str] = stops[skip : skip + limit]
    return {
        "route_number": route_number,
        "stops": selected_stops,
        "limit": limit,
        "skip": skip,
    }
    
    
@app.get("/buses/{plate}")
def get_bus(plate: plate) -> dict[str, Any]:
    """Return details for one bus by its plate"""
    bus: dict[str, Any] | None = next(
        (item for item in DATA["buses"] if item["plate"] == plate), None
    )
    if bus is None:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus


@app.get("/fleet/{bus_type}")
def get_fleet(bus_type: BusType) -> list[dict[str, Any]]:
    """Return all buses belonging to one supported bus type"""
    return [bus for bus in DATA["buses"] if bus["bus_type"] == bus_type]


@app.get("/search")
def search_routes(
        destination: Annotated[
            str,
            Query(
                min_length=3,
                max_length=30,
                title="Destination",
                description="Destination to search for in route stops.",
            ),
        ],
        max_fare: Annotated[
             int | None,
             Query(
                 gt=0,
                 title="Maximum Fare",
                 description="Optional Maximum fare in Naira. Must be greater than zero.",
             ),
         ] = None,
          sort: Annotated[
        Literal["fare"] | None,
        Query(
            title="Sort option",
            description="Optional sorting option. Use 'fare' to sort by fare.",
        ),
    ] = None,
) -> list[dict[str, Any]]:
    """Find routes containing the requested destination."""
    destination_lower: str = destination.lower()

    results: list[dict[str, Any]] = [
        route
        for route in DATA["routes"]
        if any(stop.lower() == destination_lower for stop in route["stops"])
        and (max_fare is None or route["fare_naira"] <= max_fare)
    ]

    if sort == "fare":
        results.sort(key=lambda route: route["fare_naira"])

    return results


@app.get("/routes/{route_number}/buses")
def get_route_buses(route_number: RouteNumber) -> list[dict[str, Any]]:
    """Return every bus serving one route."""
    return [
        bus
        for bus in DATA["buses"]
        if bus["route_number"] == route_number
    ]