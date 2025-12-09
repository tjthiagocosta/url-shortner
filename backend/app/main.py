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

# Import services
from app.services import (
    create_short_url,
    get_url_by_key,
    track_url_visit,
    get_url_stats,
    get_location_data,
)


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


class ShortenResponse(BaseModel):
    """
    Response model for URL shortening request.

    Attributes:
        short_url: The shortened URL that redirects to the original
    """

    short_url: str


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


@app.post("/shorten", response_model=ShortenResponse, status_code=201, tags=["URL"])
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):
    """
    Create a shortened URL from a long URL.
    """
    original_url = str(url_input.url).rstrip("/")
    return create_short_url(db, original_url)


@app.get("/{short_key}", tags=["URL"])
async def redirect_to_url(
    short_key: str, request: Request, db: Session = Depends(get_db)
):
    """
    Redirect to the original URL and track visit information.
    """
    url = get_url_by_key(db, short_key)
    if url:
        ip = request.headers.get("x-forwarded-for") or request.client.host
        user_agent = request.headers.get("user-agent", "")
        location = await get_location_data(ip)
        track_url_visit(db, url, ip, location, user_agent)
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")


@app.get("/stats/{short_key}", response_model=URLResponse, tags=["Analytics"])
async def get_url_stats(short_key: str, db: Session = Depends(get_db)):
    """
    Get analytics for a shortened URL.
    """
    url = get_url_by_key(db, short_key)
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
