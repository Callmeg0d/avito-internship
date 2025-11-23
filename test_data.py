"""
Запускается автоматически после миграций или вручную: python test_data.py
"""

import asyncio
from datetime import datetime
from app.database import async_session_maker
from app.models.team import Team
from app.models.user import User
from app.models.pull_request import PullRequest, PullRequestReviewer, PRStatus


async def create_test_data():
    """Создание тестовых данных напрямую в БД"""
    async with async_session_maker() as session:
        try:
            team = Team(team_name="backend")
            session.add(team)
            await session.flush()

            users_data = [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True},
                {"user_id": "u3", "username": "Charlie", "is_active": True}
            ]
            users = []
            for user_data in users_data:
                user = User(
                    user_id=user_data["user_id"],
                    username=user_data["username"],
                    is_active=user_data["is_active"],
                    team_name="backend"
                )
                session.add(user)
                users.append(user)
            await session.flush()

            # Создаем PR от Alice
            pr1 = PullRequest(
                pull_request_id="pr-1",
                pull_request_name="Add authentication",
                author_id="u1",
                status=PRStatus.OPEN,
                created_at=datetime.utcnow()
            )
            session.add(pr1)
            await session.flush()

            # Назначаем ревьюверов (Bob и Charlie)
            reviewer1 = PullRequestReviewer(
                id="pr-1_u2",
                pull_request_id="pr-1",
                reviewer_id="u2"
            )
            reviewer2 = PullRequestReviewer(
                id="pr-1_u3",
                pull_request_id="pr-1",
                reviewer_id="u3"
            )
            session.add(reviewer1)
            session.add(reviewer2)
            print(f"Назначены ревьюверы: u2, u3")

            # Создаем PR от Bob
            pr2 = PullRequest(
                pull_request_id="pr-2",
                pull_request_name="Fix bug in API",
                author_id="u2",
                status=PRStatus.OPEN,
                created_at=datetime.utcnow()
            )
            session.add(pr2)
            await session.flush()

            # Назначаем ревьюверов (Alice и Charlie)
            reviewer3 = PullRequestReviewer(
                id="pr-2_u1",
                pull_request_id="pr-2",
                reviewer_id="u1"
            )
            reviewer4 = PullRequestReviewer(
                id="pr-2_u3",
                pull_request_id="pr-2",
                reviewer_id="u3"
            )
            session.add(reviewer3)
            session.add(reviewer4)
            print(f"Назначены ревьюверы: u1, u3")

            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Ошибка при создании тестовых данных: {e}")
            # Игнорируем ошибки, если данные уже существуют
            if "already exists" not in str(e).lower():
                raise


if __name__ == "__main__":
    asyncio.run(create_test_data())

