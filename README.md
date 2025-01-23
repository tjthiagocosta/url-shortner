# URL Shortener API

This is a FastAPI-based URL Shortener application that allows users to shorten URLs, track access analytics, and retrieve statistics. The project includes features such as geolocation tracking for URL visits and an integrated test suite.

---

## Features
- Shorten long URLs into short, easy-to-use links.
- Redirect users to the original URL via the shortened URL.
- Analytics: Track the number of accesses and geolocation information (city, country, coordinates) for each shortened URL.
- Health check endpoint for verifying the API status.
- Fully tested with unit and integration tests.

---

## Requirements
- Python 3.9 or later
- FastAPI
- SQLAlchemy
- Pydantic
- pytest (for testing)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tjthiagocosta/url-shortner.git
   cd url-shortner
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   pip install -r requirements.txt
   ```

3. Set environment variables (optional):
   ```bash
   export API_HOST="http://localhost:8000"
   export ALLOWED_ORIGINS="http://localhost:3000"
   ```

---

## Usage

### Run the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### API Endpoints
- `GET /`: Health check.
- `POST /shorten`: Shorten a URL.
  - Request Body: `{ "url": "https://example.com" }`
  - Response: `{ "short_url": "http://localhost:8000/<short_key>" }`
- `GET /{short_key}`: Redirect to the original URL.
- `GET /stats/{short_key}`: Retrieve analytics for the shortened URL.

---

## Testing

1. Set up the test database:
   ```bash
   export SQLALCHEMY_TEST_DATABASE_URL="sqlite:///./test.db"
   ```

2. Run the test suite:
   ```bash
   pytest
   ```

---

## Project Structure
```
URL-SHORTNER/
│
├── app/
│   ├── __pycache__/         # Python cache files
│   ├── __init__.py          # App initialization
│   ├── config.py            # Application configuration
│   ├── database.py          # Database connection and session management
│   ├── main.py              # Main application logic
│   ├── models.py            # SQLAlchemy models for URL and URLLocation
│
├── tests/
│   ├── __pycache__/         # Test cache files
│   ├── __init__.py          # Test module initialization
│   ├── test_main.py         # Test suite for the application
│
├── venv/                    # Virtual environment files
│
├── .env                     # Environment variables
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── requirements.txt         # Project dependencies
├── requirements-dev.txt     # Development dependencies
```

---

## Future Enhancements
- Add a user authentication system for managing URLs.
- Enable custom short keys for URLs.
- Improve geolocation accuracy by integrating with more reliable APIs.
- Add advanced analytics (e.g., browser/device information).

---

## License
This project is licensed under the MIT License.

---

## Author
Thiago Costa

For any questions or contributions, feel free to reach out.

