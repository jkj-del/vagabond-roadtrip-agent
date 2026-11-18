import json
import logging

logger = logging.getLogger("vagabond_agent")

def calculate_route_distance(origin: str, destination: str) -> str:
    """
    Calculates the driving distance and time between two European cities.
    
    Args:
        origin (str): Starting city (e.g., 'Munich')
        destination (str): Ending city (e.g., 'Innsbruck')
        
    Returns:
        str: JSON string containing distance, driving duration, and EV status.
    """
    try:
        if not origin or not destination:
            raise ValueError("Origin and destination must be non-empty strings.")
        
        # Simulated distance mapping for European routes
        mock_routes = {
            ("Munich", "Innsbruck"): {"distance_km": 151, "duration_hours": 2.0},
            ("Innsbruck", "Cortina"): {"distance_km": 160, "duration_hours": 2.5},
            ("Cortina", "Munich"): {"distance_km": 300, "duration_hours": 4.0}
        }
        
        route_key = (origin, destination)
        route_data = mock_routes.get(route_key, {"distance_km": 100, "duration_hours": 1.5})
        
        # Verify EV constraint: Warn if distance > 250km without suggesting a charge stop
        route_data["ev_warning"] = "Requires EV mid-charge stop" if route_data["distance_km"] > 250 else "No warning"
        
        return json.dumps(route_data)
        
    except Exception as e:
        logger.error(f"Error calculating route: {str(e)}")
        return json.dumps({"error": "Failed to calculate route", "details": str(e)})
