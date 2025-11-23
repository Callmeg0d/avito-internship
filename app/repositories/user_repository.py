from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_active_by_team(self, team_name: str, exclude_user_id: Optional[str] = None) -> List[User]:
        query = select(User).where(
            User.team_name == team_name,
            User.is_active == True
        )
        if exclude_user_id:
            query = query.where(User.user_id != exclude_user_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create_or_update(self, user: User) -> User:
        existing = await self.get_by_id(str(user.user_id))
        if existing:
            existing.username = str(user.username)  # type: ignore[assignment]
            existing.is_active = bool(user.is_active)  # type: ignore[assignment]
            existing.team_name = str(user.team_name)  # type: ignore[assignment]
            return existing
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_activity(self, user_id: str, is_active: bool) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user:
            user.is_active = is_active  # type: ignore[assignment]
            await self.session.flush()
        return user

