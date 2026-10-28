import os
import tempfile

_TMP_DIR = tempfile.mkdtemp(prefix="uefa_test_")

# Uygulama import edilmeden önce test ortamı değişkenleri (gerçek .env/DB kullanılmaz)
os.environ.update({
    "APP_NAME": "UEFA Draw API",
    "APP_VERSION": "1.0.0",
    "DEBUG": "False",
    "API_V1_STR": "/api/v1",
    "PROJECT_NAME": "UEFA Competition Draw System",
    "DATABASE_URL": f"sqlite+aiosqlite:///{_TMP_DIR}/test.db",
    "BACKEND_CORS_ORIGINS": '["http://localhost:3000"]',
    "SECRET_KEY": "test-secret",
    "ACCESS_TOKEN_EXPIRE_MINUTES": "30",
    "UEFA_API_BASE_URL": "http://localhost.invalid",
    "LOG_LEVEL": "INFO",
})

import httpx  # noqa: E402
import pytest_asyncio  # noqa: E402

from core.dependencies import get_db_session  # noqa: E402
from infrastructure.database import models  # noqa: E402,F401
from infrastructure.database.connection import DatabaseConnection  # noqa: E402
from main import app  # noqa: E402


@pytest_asyncio.fixture
async def test_db():
    db = DatabaseConnection(os.environ["DATABASE_URL"])
    await db.drop_tables()
    await db.create_tables()
    yield db
    await db.drop_tables()
    await db.close()


@pytest_asyncio.fixture
async def client(test_db):
    async def override_session():
        async for session in test_db.get_session():
            yield session

    app.dependency_overrides[get_db_session] = override_session
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


_COUNTRIES = ["ESP", "ENG", "GER", "ITA", "FRA", "POR", "NED", "BEL", "TUR", "SCO", "AUT", "SUI", "GRE", "CZE", "UKR"]


def make_teams():
    """36 takım, her potta 9."""
    return [
        {
            "id": i,
            "name": f"Team {i}",
            "country": _COUNTRIES[i % len(_COUNTRIES)],
            "pot": (i - 1) // 9 + 1,
            "coefficient": float(200 - i),
        }
        for i in range(1, 37)
    ]
