from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base
from datetime import datetime

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_url_key = Column(String(10), unique=True, index=True, nullable=False)
    original_url = Column(String, nullable=False)
    access_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_accessed = Column(DateTime, nullable=True)
