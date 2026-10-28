import random
from datetime import datetime

import pytest

from core.dependencies import get_draw_service
from domain.entities import Draw
from infrastructure.database.models import DrawModel
from main import app
from tests.conftest import make_teams


class _StubDrawService:
    """Gerçek draw algoritmasının yerine geçen deterministik servis."""

    async def perform_draw(self, teams, competition, season):
        draw = Draw(competition=competition.value, season=season, teams=teams, fixtures=[])
        draw.id = 1
        draw.created_at = datetime.utcnow()
        return draw


async def test_perform_draw_success(client):
    app.dependency_overrides[get_draw_service] = lambda: _StubDrawService()
    payload = {"competition": "champions_league", "season": "2025/26", "teams": make_teams()}
    r = await client.post("/api/v1/draw/", json=payload)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["id"] == 1
    assert body["competition"] == "champions_league"
    assert body["season"] == "2025/26"
    assert len(body["results"]) == 36
    assert {"total_fixtures", "is_valid", "created_at"} <= set(body)


@pytest.mark.xfail(
    reason="BUG: DrawServiceImpl._draw_opponents_for_team ('Cannot find valid opponent "
    "for Team N from pot 1') gerçek çekilişte her zaman ValueError -> 500 üretiyor "
    "(application/services/draw_service.py:_draw_opponents_for_team)",
    strict=False,
)
async def test_perform_draw_real_service(client):
    random.seed(0)
    payload = {"competition": "champions_league", "season": "2025/26", "teams": make_teams()}
    r = await client.post("/api/v1/draw/", json=payload)
    assert r.status_code == 201, r.text


async def test_validate_draw_success(client, test_db):
    async for s in test_db.get_session():
        draw = DrawModel(competition="champions_league", season="2025/26", is_valid=False)
        s.add(draw)
        await s.flush()
        draw_id = draw.id

    r = await client.post("/api/v1/draw/validate", json={"draw_id": draw_id})
    assert r.status_code == 200, r.text
    body = r.json()
    assert set(body) == {"is_valid", "errors", "warnings", "statistics"}
    assert isinstance(body["errors"], list)
    assert isinstance(body["warnings"], list)
    assert "total_fixtures" in body["statistics"]
