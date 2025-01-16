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
    city: str
    country: str
    coordinates: dict
    accessed_at: datetime


class URLResponse(BaseModel):
    short_url: str
    original_url: str
    created_at: datetime
    access_count: int
    locations: List[LocationResponse]


class URLInput(BaseModel):
    url: HttpUrl


# Generate a short URL key
def generate_short_key(length: int = 6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


async def get_location_data(ip_address: str) -> dict:
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
    Health check endpoint.
    """
    return {
        "status": "healthy",
        "version": app.version,
        "documentation": f"{API_HOST}/docs",
    }


@app.post("/shorten")
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):
    short_key = generate_short_key()
    new_url = URL(short_url_key=short_key, original_url=url_input.url)
    db.add(new_url)
    db.commit()
    return {"short_url": f"http://localhost:8000/{short_key}"}


@app.get("/{short_key}")
async def redirect_to_url(
    short_key: str, request: Request, db: Session = Depends(get_db)
):
    url = db.query(URL).filter(URL.short_url_key == short_key).first()
    if url:
        ip = request.headers.get("x-forwarded-for") or request.client.host
        location = await get_location_data(ip)

        if location:
            url_location = URLLocation(
                url_id=url.id,
                ip_address=ip,
                city=location["city"],
                country=location["country"],
                latitude=location["lat"],
                longitude=location["lon"],
            )
            db.add(url_location)
            db.commit()

        url.access_count += 1
        db.commit()
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")


@app.get("/stats/{short_key}", response_model=URLResponse, tags=["Analytics"])
async def get_url_stats(short_key: str, db: Session = Depends(get_db)):
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
