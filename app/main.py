from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.models import Base, URL, URLLocation
from app.database import engine, get_db
import string
import random
import os
from pydantic import BaseModel, HttpUrl
from starlette.responses import RedirectResponse
from datetime import datetime
from typing import List
import requests

# Load environment variables
API_HOST = os.getenv("API_HOST", "http://localhost:8000")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to shorten URLs and redirect users.",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


class LocationResponse(BaseModel):
    """
    Response model for location information.

    Attributes:
        city: Name of the city
        country: Name of the country
        coordinates: Dictionary containing latitude and longitude
        accessed_at: Timestamp of when the URL was accessed
    """

    city: str
    country: str
    coordinates: dict
    accessed_at: datetime


class URLResponse(BaseModel):
    """
    Response model for URL information including analytics.

    Attributes:
        short_url: The shortened URL
        original_url: The original URL that was shortened
        created_at: Timestamp of when the URL was created
        access_count: Number of times the URL has been accessed
        locations: List of locations from where the URL was accessed
    """

    short_url: str
    original_url: str
    created_at: datetime
    access_count: int
    locations: List[LocationResponse]


class URLInput(BaseModel):
    """
    Input model for URL shortening request.

    Attributes:
        url: The URL to be shortened (must be a valid HTTP/HTTPS URL)
    """

    url: HttpUrl


def generate_short_key(length: int = 6) -> str:
    """
    Generate a random short key for URL shortening.

    Args:
        length: Length of the short key (default: 6)

    Returns:
        str: Random string of specified length containing letters and numbers
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


async def get_location_data(ip_address: str) -> dict:
    """
    Get geolocation data for an IP address using ip-api.com.

    Args:
        ip_address: IP address to look up

    Returns:
        dict: Location data including city, country, latitude, and longitude
              Returns None if the request fails or data is invalid
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


@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint to verify API status.

    Returns:
        dict: API status information including version and documentation URL
    """
    return {
        "status": "healthy",
        "version": app.version,
        "documentation": f"{API_HOST}/docs",
    }


@app.post("/shorten")
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):
    """
    Create a shortened URL from a long URL.

    Args:
        url_input: URLInput model containing the URL to shorten
        db: Database session

    Returns:
        dict: Contains the shortened URL
    """
    short_key = generate_short_key()
    original_url = str(url_input.url).rstrip("/")
    new_url = URL(short_url_key=short_key, original_url=original_url)
    db.add(new_url)
    db.commit()
    return {"short_url": f"{API_HOST}/{short_key}"}


@app.get("/{short_key}")
async def redirect_to_url(
    short_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Redirect to the original URL and track visit information.

    Args:
        short_key: The short key of the URL
        request: FastAPI request object containing client information
        db: Database session

    Returns:
        RedirectResponse: Redirects to the original URL

    Raises:
        HTTPException: If the URL is not found (404)
    """
    url = db.query(URL).filter(URL.short_url_key == short_key).first()
    if url:
        ip = request.headers.get("x-forwarded-for") or request.client.host
        location = await get_location_data(ip)

        # Create URL location with default values if location data is missing
        url_location = URLLocation(
            url_id=url.id,
            ip_address=ip,
            city=location["city"] if location else "Unknown",
            country=location["country"] if location else "Unknown",
            latitude=location["lat"] if location else 0.0,
            longitude=location["lon"] if location else 0.0,
        )
        db.add(url_location)
        db.commit()

        url.access_count += 1
        db.commit()
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")


@app.get("/stats/{short_key}", response_model=URLResponse, tags=["Analytics"])
async def get_url_stats(short_key: str, db: Session = Depends(get_db)):
    """
    Get analytics for a shortened URL.

    Args:
        short_key: The short key of the URL
        db: Database session

    Returns:
        URLResponse: URL information including visit statistics and locations

    Raises:
        HTTPException: If the URL is not found (404)
    """
    url = db.query(URL).filter(URL.short_url_key == short_key).first()
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    locations = [
        LocationResponse(
            city=loc.city,
            country=loc.country,
            coordinates={"lat": loc.latitude, "lon": loc.longitude},
            accessed_at=loc.accessed_at,
        )
        for loc in url.locations
    ]

    return URLResponse(
        short_url=f"{API_HOST}/{short_key}",
        original_url=url.original_url,
        created_at=url.created_at,
        access_count=url.access_count,
        locations=locations,
    )
