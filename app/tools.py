import json
import logging

logger = logging.getLogger("vagabond_agent")

ROUTE_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "origin": {"type": "string", "minLength": 2},
        "destination": {"type": "string", "minLength": 2}
    },
    "required": ["origin", "destination"]
}

def validate_schema(data: dict, schema: dict) -> bool:
    """Manual schema validator for inputs/outputs."""
    for prop, rules in schema.get("properties", {}).items():
        if prop not in data and prop in schema.get("required", []):
            return False
        if prop in data:
            if rules.get("type") == "string" and not isinstance(data[prop], str):
                return False
            if "minLength" in rules and len(data[prop]) < rules["minLength"]:
                return False
    return True

def calculate_route_distance(origin: str, destination: str) -> str:
    """
    Calculates the driving distance and time between two European cities with schema validation.
    """
    input_data = {"origin": origin, "destination": destination}
    
    # 1. JSON input validation
    if not validate_schema(input_data, ROUTE_INPUT_SCHEMA):
        return json.dumps({
            "error": "INVALID_INPUT_SCHEMA",
            "recovery_instruction": "The provided cities are empty or too short. Please ask the user to specify complete city names with at least 2 characters."
        })
        
    try:
        mock_routes = {
            ("Munich", "Innsbruck"): {"distance_km": 151, "duration_hours": 2.0},
            ("Innsbruck", "Cortina"): {"distance_km": 160, "duration_hours": 2.5},
            ("Cortina", "Munich"): {"distance_km": 300, "duration_hours": 4.0}
        }
        
        route_key = (origin, destination)
        if route_key not in mock_routes:
            raise KeyError(f"Route from {origin} to {destination} is not mapped.")
            
        route_data = mock_routes[route_key]
        route_data["ev_warning"] = "Requires EV mid-charge stop" if route_data["distance_km"] > 250 else "No warning"
        return json.dumps(route_data)
        
    except KeyError as ke:
        return json.dumps({
            "error": "ROUTE_NOT_FOUND",
            "recovery_instruction": f"The route '{origin} to {destination}' is outside our active database. Please suggest an alternative route via Munich or Innsbruck."
        })
    except Exception as e:
        return json.dumps({
            "error": "SYSTEM_EXCEPTION",
            "recovery_instruction": "An internal system error occurred. Please try repeating the query using fallback inputs."
        })
