import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import URL, URLLocation
from app.config import settings
from datetime import datetime

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_location_data():
    return {
        "status": "success",
        "city": "Test City",
        "country": "Test Country",
        "lat": 12.345,
        "lon": 67.890,
    }


class TestHealthCheck:
    def test_health_check(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {
            "status": "healthy",
            "version": "1.0.0",
            "documentation": f"{settings.api_host}/docs",
        }


class TestURLShortener:
    def test_shorten_valid_url(self):
        test_url = "https://www.example.com"
        response = client.post("/shorten", json={"url": test_url})
        assert response.status_code == 200
        assert "short_url" in response.json()
        assert response.json()["short_url"].startswith(f"{settings.api_host}/")

    def test_shorten_invalid_url(self):
        # Test both invalid format and empty URL
        for invalid_url in ["invalid-url", ""]:
            response = client.post("/shorten", json={"url": invalid_url})
            assert response.status_code == 422


class TestRedirection:
    @patch("requests.get")
    def test_redirect_success(self, mock_get, mock_location_data):
        test_url = "https://www.example.com"
        response = client.post("/shorten", json={"url": test_url})
        short_key = response.json()["short_url"].split("/")[-1]

        # Mock location API response
        mock_get.return_value.json.return_value = mock_location_data

        response = client.get(f"/{short_key}", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == test_url

    def test_redirect_nonexistent_url(self):
        response = client.get("/nonexistent", follow_redirects=False)
        assert response.status_code == 404

    @patch("requests.get")
    def test_redirect_failed_location_api(self, mock_get):
        # Create shortened URL
        test_url = "https://www.example.com"
        response = client.post("/shorten", json={"url": test_url})
        short_key = response.json()["short_url"].split("/")[-1]

        # Mock failed API response
        mock_get.side_effect = Exception("API Error")

        # Should still redirect despite location API failure
        response = client.get(f"/{short_key}", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == test_url


class TestStats:
    @patch("requests.get")
    def test_stats_with_locations(self, mock_get, mock_location_data):
        test_url = "https://www.example.com"
        response = client.post("/shorten", json={"url": test_url})
        short_key = response.json()["short_url"].split("/")[-1]

        mock_get.return_value.json.return_value = mock_location_data
        client.get(f"/{short_key}")

        response = client.get(f"/stats/{short_key}")
        assert response.status_code == 200
        data = response.json()
        assert data["original_url"] == test_url
        assert data["access_count"] == 1
        assert len(data["locations"]) == 1
        assert data["locations"][0]["city"] == "Test City"
        assert data["locations"][0]["country"] == "Test Country"
        assert data["locations"][0]["coordinates"] == {"lat": 12.345, "lon": 67.890}

    def test_stats_nonexistent_url(self):
        response = client.get("/stats/nonexistent")
        assert response.status_code == 404

    def test_stats_no_visits(self):
        # Create URL without visiting it
        test_url = "https://www.example.com"
        response = client.post("/shorten", json={"url": test_url})
        short_key = response.json()["short_url"].split("/")[-1]

        response = client.get(f"/stats/{short_key}")
        assert response.status_code == 200
        assert response.json()["access_count"] == 0
        assert len(response.json()["locations"]) == 0


class TestLocationHandling:
    @patch("requests.get")
    def test_location_error_handling(self, mock_get):
        # Test both missing data and API error
        test_url = "https://www.example.com"
        response = client.post("/shorten", json={"url": test_url})
        short_key = response.json()["short_url"].split("/")[-1]

        # Test missing data
        mock_get.return_value.json.return_value = None
        client.get(f"/{short_key}")

        # Test API error
        mock_get.side_effect = Exception("API Error")
        client.get(f"/{short_key}")

        # Check stats
        response = client.get(f"/stats/{short_key}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["locations"]) == 2
        for location in data["locations"]:
            assert location["city"] == "Unknown"
            assert location["country"] == "Unknown"
            assert location["coordinates"] == {"lat": 0.0, "lon": 0.0}
