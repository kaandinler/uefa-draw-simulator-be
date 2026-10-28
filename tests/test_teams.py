from infrastructure.database.models import TeamModel


async def test_get_teams_success(client, test_db):
    async for s in test_db.get_session():
        s.add(TeamModel(id=1, name="Real Madrid", country="ESP", pot=1, coefficient=148.0))
        s.add(TeamModel(id=2, name="Liverpool", country="ENG", pot=1, coefficient=141.0))

    r = await client.get("/api/v1/teams/champions_league")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert {t["name"] for t in data} == {"Real Madrid", "Liverpool"}
    assert set(data[0]) >= {"id", "name", "country", "pot", "coefficient"}
