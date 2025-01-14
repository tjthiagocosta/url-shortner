from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to shorten URLs and redirect users.",
    version="1.0.0",
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Welcome to the URL Shortener API"}
