# URL Shortener Pro

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

A full-stack URL shortening service with advanced analytics capabilities, featuring a FastAPI backend and modern React frontend.


## ✨ Features

### Backend Services

- **URL Shortening**
  - Generate unique short codes
  - High-performance redirects
  - Custom slug support
- **Analytics Engine**
  - Real-time click tracking
  - Device detection (Mobile/Desktop/Tablet)
  - Browser & OS identification
  - Bot detection
  - Geolocation tracking
- **Security**
  - Rate limiting
  - URL validation
  - Expiring links
- **API**
  - RESTful endpoints
  - OpenAPI documentation
  - JWT Authentication

### Frontend (In Development)

- Modern dashboard UI
- Real-time analytics visualization
- URL management interface
- Responsive design
- Dark/Light mode

## 🛠 Tech Stack

**Backend**  
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green?logo=fastapi)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red?logo=python&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Caching-yellow?logo=redis)

**Frontend**  
![React](https://img.shields.io/badge/React-18+-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript&logoColor=white)
![Shadcn/ui](https://img.shields.io/badge/Shadcn/ui-0.5+-18181b?logo=ui)



## 📂 Project Structure

```
url-shortener-pro/
├── backend/               # FastAPI backend
│   ├── app/               # Application core
│   │   ├── models/        # Database models
│   │   ├── services/      # Business logic
│   │   ├── routes/        # API endpoints
│   │   ├── core/          # Configuration & utils
│   │   └── main.py        # Application entrypoint
│   ├── tests/             # Test suite
│   └── requirements.txt   # Dependencies
│
└── frontend/              # React frontend
    ├── public/            # Static assets
    ├── src/               # Application source
    │   ├── components/    # UI components
    │   ├── hooks/         # Custom hooks
    │   ├── lib/           # Utilities
    │   ├── types/         # Type definitions
    │   └── main.tsx       # Application entrypoint
    ├── package.json       # Frontend dependencies
    └── tsconfig.json     # TypeScript config
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- SQLite3

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/MacOS
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
pnpm install
pnpm dev
```

## 🌐 API Documentation

Access interactive API docs at `http://localhost:8000/docs`

### Example Request

```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Example Response

```json
{
  "short_url": "http://localhost:8000/abc123",
  "analytics": {
    "access_count": 42,
    "devices": { "mobile": 15, "desktop": 27 },
    "locations": [
      {
        "city": "New York",
        "country": "US",
        "coordinates": { "lat": 40.7128, "lon": -74.006 }
      }
    ]
  }
}
```

## 📈 Roadmap

- [x] Core URL shortening functionality
- [x] Basic analytics tracking
- [ ] User authentication system
- [ ] Admin dashboard
- [ ] API rate limiting
- [ ] Bulk URL import/export
- [ ] QR code generation

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Project Maintainers**  
[Thiago Costa](https://github.com/tjthiagocosta)  

