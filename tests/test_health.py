async def test_root(client):
    r = await client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "UEFA Competition Draw System"
    assert body["version"] == "1.0.0"
    assert body["docs"] == "/docs"
    assert body["health"] == "/api/v1/health"


async def test_health(client):
    r = await client.get("/api/v1/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


async def test_ready(client):
    r = await client.get("/api/v1/health/ready")
    assert r.status_code == 200
    assert r.json() == {"status": "ready", "database": "connected"}
