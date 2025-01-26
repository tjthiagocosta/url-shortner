# URL Shortener Full Stack Application

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

A modern, full-stack URL shortening service featuring a FastAPI backend and React frontend, with comprehensive analytics including device tracking and geolocation insights.

## Features

### Backend

- 🚀 High-performance URL shortening with FastAPI
- 📊 Advanced analytics tracking:
  - 📱 Device information (mobile/desktop/tablet)
  - 🌐 Browser and OS detection
  - 🤖 Bot detection
  - 🌍 Geolocation tracking
- 🔄 RESTful API endpoints
- 📝 OpenAPI documentation

### Frontend (Under Construction)

- ⚛️ Modern React with TypeScript
- 🎨 Sleek UI with Tailwind CSS
- 📱 Responsive design
- 🌙 Dark mode support (planned)

## Technology Stack

### Backend

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Analytics**:
  - User-Agents (device detection)
  - IP-API.com (geolocation)

### Frontend

- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Package Manager**: pnpm

## Project Structure

```
url-shortener/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── device_service.py
│   │   │   ├── location_service.py
│   │   │   └── url_service.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── database.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## Getting Started

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Configure environment variables in `backend/.env`:

```env
DATABASE_URL=sqlite:///./data/url_shortener.db
API_HOST=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend Setup

```bash
cd frontend
pnpm install
pnpm dev
```

## API Endpoints

### Core Endpoints

- `GET /` - Health check
- `POST /shorten` - Create short URL
- `GET /{short_key}` - Redirect to original URL
- `GET /stats/{short_key}` - Get URL analytics

### Analytics Response Example

```json
{
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://example.com",
  "created_at": "2024-01-01T12:00:00",
  "access_count": 42,
  "locations": [
    {
      "city": "New York",
      "country": "United States",
      "coordinates": {
        "lat": 40.7128,
        "lon": -74.006
      },
      "accessed_at": "2024-01-01T12:00:00"
    }
  ],
  "device_info": {
    "device_type": "mobile",
    "browser": "Chrome",
    "os": "iOS",
    "is_bot": false
  }
}
```

## Development Status

- ✅ Backend API complete
- 🚧 Frontend under construction
- 📱 Device analytics implemented
- 🌍 Geolocation tracking active
- 🎨 UI/UX design in progress

## Roadmap

- [ ] User authentication
- [ ] Custom URL slugs
- [ ] QR code generation
- [ ] QR code customization
- [ ] Advanced analytics dashboard
- [ ] Rate limiting
- [ ] Dockerize application

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Thiago Costa

## Support

For support or questions, please open an issue in the GitHub repository.
