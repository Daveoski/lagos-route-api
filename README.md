# Lagos Route Window

[![wakatime](https://wakatime.com/badge/user/c09aeb97-ea88-48f4-835d-eb89deb4951a/project/17cb0de7-e8f1-40de-b18d-b5bda6b1af61.svg)](https://wakatime.com/badge/user/c09aeb97-ea88-48f4-835d-eb89deb4951a/project/17cb0de7-e8f1-40de-b18d-b5bda6b1af61)

A read-only **FastAPI** service for looking up Lagos bus routes, stops and buses. The data comes from a JSON file that is loaded at startup.

## Features

- Route and bus counts
- Stops on a route
- Search routes by destination, or filter them by maximum fare
- Look up a bus by plate number
- Filter the fleet by bus type
- List the buses serving a route
- Input validation with FastAPI `Path` and `Query`
- Automatic Swagger UI docs

## Getting started

```bash
# with uv
uv sync
uv run fastapi dev main.py

# or with pip
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs.

## Endpoints

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/` | Service summary with route and bus counts |
| GET | `/route/{route_number}/stops` | Stops on a route |
| GET | `/search` | Search routes by destination or maximum fare |
| GET | `/buses/{plate}` | Bus details by plate number |
| GET | `/fleet/{bus_type}` | Buses of a given type |
| GET | `/routes/{route_number}/buses` | Buses serving a route |

## Project structure

```text
├── main.py             # FastAPI app and endpoints
├── data.py             # Loads lagos_routes.json
├── lagos_routes.json   # Route and bus data
├── pyproject.toml
└── requirements.txt
```

## License

[MIT](LICENSE)
