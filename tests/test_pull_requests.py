import pytest


@pytest.mark.asyncio
async def test_create_pr_with_auto_reviewers(client):
    await client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True},
                {"user_id": "u3", "username": "Charlie", "is_active": True}
            ]
        }
    )

    response = await client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr-1",
            "pull_request_name": "Test PR",
            "author_id": "u1"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["pr"]["pull_request_id"] == "pr-1"
    assert data["pr"]["status"] == "OPEN"
    assert len(data["pr"]["assigned_reviewers"]) <= 2
    assert "u1" not in data["pr"]["assigned_reviewers"]  # Автор не должен быть ревьювером


@pytest.mark.asyncio
async def test_merge_pr(client):
    await client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True}
            ]
        }
    )
    
    await client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr-1",
            "pull_request_name": "Test PR",
            "author_id": "u1"
        }
    )
    
    # Merge PR
    response = await client.post(
        "/pullRequest/merge",
        json={"pull_request_id": "pr-1"}
    )
    
    assert response.status_code == 200
    assert response.json()["pr"]["status"] == "MERGED"
    assert response.json()["pr"]["mergedAt"] is not None


@pytest.mark.asyncio
async def test_merge_pr_idempotent(client):
    await client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True}
            ]
        }
    )
    
    await client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr-1",
            "pull_request_name": "Test PR",
            "author_id": "u1"
        }
    )

    response1 = await client.post(
        "/pullRequest/merge",
        json={"pull_request_id": "pr-1"}
    )
    assert response1.status_code == 200
    
    # Второй merge (должен быть идемпотентным)
    response2 = await client.post(
        "/pullRequest/merge",
        json={"pull_request_id": "pr-1"}
    )
    assert response2.status_code == 200
    assert response2.json()["pr"]["status"] == "MERGED"


@pytest.mark.asyncio
async def test_reassign_reviewer(client):
    await client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True},
                {"user_id": "u3", "username": "Charlie", "is_active": True}
            ]
        }
    )
    
    # Создаем PR
    await client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr-1",
            "pull_request_name": "Test PR",
            "author_id": "u1"
        }
    )
    
    # Переназначаем ревьювера
    response = await client.post(
        "/pullRequest/reassign",
        json={
            "pull_request_id": "pr-1",
            "old_user_id": "u2"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "replaced_by" in data
    assert data["replaced_by"] != "u2"
    assert data["pr"]["status"] == "OPEN"


@pytest.mark.asyncio
async def test_reassign_merged_pr_fails(client):
    """Тест, что нельзя переназначить ревьювера в MERGED PR"""
    await client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True}
            ]
        }
    )
    
    await client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr-1",
            "pull_request_name": "Test PR",
            "author_id": "u1"
        }
    )
    
    # Merge PR
    await client.post(
        "/pullRequest/merge",
        json={"pull_request_id": "pr-1"}
    )
    
    # Пытаемся переназначить - должно быть ошибка
    response = await client.post(
        "/pullRequest/reassign",
        json={
            "pull_request_id": "pr-1",
            "old_user_id": "u2"
        }
    )
    
    assert response.status_code == 409
    assert response.json()["error"]["code"] == "PR_MERGED"