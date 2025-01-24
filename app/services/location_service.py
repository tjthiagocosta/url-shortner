import requests
from typing import Optional


async def get_location_data(ip_address: str) -> Optional[dict]:
    """
    Get geolocation data for an IP address using ip-api.com.
    """
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        data = response.json()
        if data.get("status") == "success":
            return {
                "city": data.get("city"),
                "country": data.get("country"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
            }
    except Exception:
        pass
    return None
