from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Base, URL
from app.database import engine, get_db
import string
import random
from pydantic import BaseModel
from starlette.responses import RedirectResponse

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to shorten URLs and redirect users.",
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Generate a short URL key
def generate_short_key(length: int = 6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.get("/")
def root():
    return {"message": "Welcome to the URL Shortener API"}

class URLInput(BaseModel):
    url: str

@app.post("/shorten")
def shorten_url(url_input: URLInput, db: Session = Depends(get_db)):
    short_key = generate_short_key()
    new_url = URL(short_url_key=short_key, original_url=url_input.url)
    db.add(new_url)
    db.commit()
    return {"short_url": f"http://localhost:8000/{short_key}"}

@app.get("/{short_key}")
def redirect_to_url(short_key: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_url_key == short_key).first()
    if url:
        url.access_count += 1
        db.commit()
        return RedirectResponse(url.original_url)
    raise HTTPException(status_code=404, detail="URL not found")
