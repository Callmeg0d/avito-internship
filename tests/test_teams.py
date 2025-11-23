import pytest


@pytest.mark.asyncio
async def test_create_team(client):
    response = await client.post(
        "/team/add",
        json={
            "team_name": "test_team",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True}
            ]
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["team"]["team_name"] == "test_team"
    assert len(data["team"]["members"]) == 2


@pytest.mark.asyncio
async def test_get_team(client):
    await client.post(
        "/team/add",
        json={
            "team_name": "test_team",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True}
            ]
        }
    )
    
    # Получаем команду
    response = await client.get("/team/get?team_name=test_team")
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "test_team"
    assert len(data["members"]) == 1


@pytest.mark.asyncio
async def test_create_duplicate_team(client):
    """Тест создания дубликата команды"""
    await client.post(
        "/team/add",
        json={
            "team_name": "test_team",
            "members": [{"user_id": "u1", "username": "Alice", "is_active": True}]
        }
    )
    
    response = await client.post(
        "/team/add",
        json={
            "team_name": "test_team",
            "members": [{"user_id": "u2", "username": "Bob", "is_active": True}]
        }
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "TEAM_EXISTS"