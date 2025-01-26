from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, UTC


class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    short_url_key = Column(String, unique=True, index=True)
    original_url = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    access_count = Column(Integer, default=0)
    locations = relationship("URLLocation", backref="url")


class URLLocation(Base):
    __tablename__ = "url_locations"
    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    ip_address = Column(String)
    city = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    accessed_at = Column(DateTime, default=lambda: datetime.now(UTC))
    user_agent = Column(String)
    device_type = Column(String)
    browser = Column(String)
    os = Column(String)
    is_bot = Column(Boolean, default=False)
