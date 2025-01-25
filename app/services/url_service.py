from sqlalchemy.orm import Session
from app.models import URL, URLLocation
from .key_generator import generate_short_key
from datetime import datetime
from typing import Optional
from .device_service import parse_user_agent


def create_short_url(db: Session, original_url: str) -> str:
    """
    Create a new short URL entry in the database.
    """
    short_key = generate_short_key()
    new_url = URL(short_url_key=short_key, original_url=original_url)
    db.add(new_url)
    db.commit()
    return short_key


def get_url_by_key(db: Session, short_key: str) -> Optional[URL]:
    """
    Retrieve a URL by its short key.
    """
    return db.query(URL).filter(URL.short_url_key == short_key).first()


def track_url_visit(
    db: Session, url: URL, ip_address: str, location: Optional[dict], user_agent: str
) -> None:
    """
    Track a URL visit with location and device information.
    """
    device_info = parse_user_agent(user_agent)

    url_location = URLLocation(
        url_id=url.id,
        ip_address=ip_address,
        city=location["city"] if location else "Unknown",
        country=location["country"] if location else "Unknown",
        latitude=location["lat"] if location else 0.0,
        longitude=location["lon"] if location else 0.0,
        user_agent=user_agent,
        device_type=device_info["device_type"],
        browser=device_info["browser"],
        os=device_info["os"],
        is_bot=device_info["is_bot"],
    )
    db.add(url_location)
    url.access_count += 1
    db.commit()


def get_url_stats(db: Session, url: URL) -> dict:
    """
    Get statistics for a URL.
    """
    return {
        "short_url": url.short_url_key,
        "original_url": url.original_url,
        "created_at": url.created_at,
        "access_count": url.access_count,
        "locations": url.locations,
    }
