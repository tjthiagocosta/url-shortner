# URL Shortener API

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A high-performance URL shortening service built with FastAPI, featuring analytics and geolocation tracking.

## Features

### Core Functionality
- 🚀 Fast URL shortening with customizable key length
- 🔗 Reliable redirection with 307 status code
- 📊 Comprehensive analytics tracking

### Analytics
- 🌍 Geolocation tracking (city, country, coordinates)
- 📈 Access count tracking
- ⏰ Timestamped access records

### Technical Features
- 🛡️ CORS support with configurable allowed origins
- 📄 OpenAPI documentation (Swagger UI & ReDoc)
- 🧪 Comprehensive test coverage
- 🐳 Docker-ready configuration

## Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (production-ready databases supported)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

### Analytics
- **Geolocation**: IP-API.com

### Testing
- **Framework**: pytest
- **Test Client**: FastAPI TestClient
- **Mocking**: unittest.mock

## Getting Started

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tjthiagocosta/url-shortener.git
   cd url-shortener
   ```

2. Set up environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file with:
   ```env
   DATABASE_URL=sqlite:///./url_shortener.db
   API_HOST=https://api.shrnq.tech
   ALLOWED_ORIGINS="https://shrnq.tech"
   ```

### Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload
```

Access the API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /` - Verify API status

### URL Shortening
- `POST /shorten` - Create a shortened URL
  - Request Body: `{ "url": "https://example.com" }`
  - Response: `{ "short_url": "https://api.shrnq.tech/<short_key>" }`

### Redirection
- `GET /{short_key}` - Redirect to original URL

### Analytics
- `GET /stats/{short_key}` - Get URL statistics
  - Response:
    ```json
    {
      "short_url": "https://api.shrnq.tech/<short_key>",
      "original_url": "https://example.com",
      "created_at": "2024-01-01T12:00:00",
      "access_count": 42,
      "locations": [
        {
          "city": "New York",
          "country": "United States",
          "coordinates": {
            "lat": 40.7128,
            "lon": -74.0060
          },
          "accessed_at": "2024-01-01T12:00:00"
        }
      ]
    }
    ```

## Testing

Run the test suite:
```bash
pytest
```

Test coverage includes:
- Unit tests for core functionality
- Integration tests for API endpoints
- Error handling scenarios
- Edge case testing

## Project Structure

```
url-shortener/
├── app/
│   ├── config.py            # Application configuration
│   ├── database.py          # Database connection
│   ├── main.py              # API endpoints
│   ├── models.py            # Database models
│   ├── services/            # Business logic
│   │   ├── url_service.py
│   │   ├── location_service.py
│   │   └── key_generator.py
├── tests/                   # Test suite
│   ├── test_main.py         # API tests
├── .env                     # Environment variables
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
```

## Deployment

### Docker
Build and run the container:
```bash
docker build -t url-shortener .
docker run -p 8000:8000 url-shortener
```

### Production Considerations
- Use a production-ready database (PostgreSQL, MySQL)
- Configure proper CORS settings
- Implement rate limiting
- Set up monitoring and logging

## Future Enhancements
- [ ] User authentication and URL management
- [ ] Custom short URLs
- [ ] Expiration dates for URLs
- [ ] Advanced analytics (browser, device, referrer)
- [ ] Rate limiting and API keys
- [ ] Bulk URL shortening

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Thiago Costa

## Support

For support or questions, please open an issue in the GitHub repository.

