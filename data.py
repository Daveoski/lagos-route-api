import json
from pathlib import Path
from typing import Any


def load_data() -> dict[str, list[dict[str, Any]]]:
    #loads the union records once when the service starts
    data_file: Path = Path(__file__).parent / "lagos_routes.json"
    
    with data_file.open("r", encoding="utf-8") as file:
        data: dict[str, list[dict[str, Any]]] = json.load(file)
    return data


DATA: dict[str, list[dict[str, Any]]] = load_data()
    