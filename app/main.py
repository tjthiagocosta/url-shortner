from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener API",
    description="A simple API to shorten URLs and redirect users.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "Welcome to the URL Shortener API"}
