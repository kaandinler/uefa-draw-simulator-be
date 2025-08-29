# UEFA Competition Draw System

A comprehensive draw system for UEFA competitions (Champions League, Europa League, Conference League) built with FastAPI using Clean Architecture principles.

## 🏗️ Architecture

This project follows Clean Architecture with the following layers:

- **Domain Layer**: Business entities, value objects, and interfaces
- **Application Layer**: Use cases, services, and DTOs
- **Infrastructure Layer**: Database, repositories, and external services
- **Presentation Layer**: API endpoints and middleware
- **Core Layer**: Configuration, dependencies, and cross-cutting concerns

## 🚀 Features

- UEFA competition draw simulation following official rules
- RESTful API with comprehensive documentation
- Clean Architecture with Dependency Injection
- Repository Pattern for data access
- In-memory and database storage options
- Comprehensive validation and error handling
- Docker support for easy deployment

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (optional, SQLite by default)
- Redis (optional, for caching)
- Docker (optional)

## 🔧 Installation

### Local Development

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   make install
   # or
   pip install -r requirements.txt
   ```

4. Copy environment variables:
   ```bash
   cp .env.example .env
   ```

5. Run the application:
   ```bash
   make dev
   # or
   uvicorn app.main:app --reload
   ```

### Docker

1. Build and run with Docker Compose:
   ```bash
   make docker-up
   # or
   docker-compose up -d
   ```

## 📚 API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

Run tests with coverage:
```bash
make test
# or
pytest tests/ -v --cov=app
```

##