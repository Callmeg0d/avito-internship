from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.repositories.user_repository import UserRepository
from app.models.pull_request import PullRequestReviewer
from app.models.user import User
from app.schemas.stats import StatsResponse, UserStats


class StatsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session)

    async def get_assignments_stats(self) -> StatsResponse:
        # Подсчитываем количество назначений для каждого пользователя
        result = await self.session.execute(
            select(
                User.user_id,
                User.username,
                func.count(PullRequestReviewer.reviewer_id).label('count')
            )
            .outerjoin(
                PullRequestReviewer,
                User.user_id == PullRequestReviewer.reviewer_id
            )
            .group_by(User.user_id, User.username)
            .order_by(func.count(PullRequestReviewer.reviewer_id).desc())
        )

        users_stats = []
        total = 0

        for row in result.all():
            count = int(row.count) if row.count is not None else 0
            total += count
            users_stats.append(
                UserStats(
                    user_id=str(row.user_id),
                    username=str(row.username),
                    assignments_count=count
                )
            )

        return StatsResponse(
            total_assignments=total,
            users=users_stats
        )
