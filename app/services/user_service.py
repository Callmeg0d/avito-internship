from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse, UserActivityUpdate
from app.exceptions import NotFoundException


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repo = UserRepository(session)

    async def set_activity(self, data: UserActivityUpdate) -> UserResponse:
        user = await self.user_repo.update_activity(data.user_id, data.is_active)
        if not user:
            raise NotFoundException("user")

        return UserResponse(
            user_id=str(user.user_id),
            username=str(user.username),
            team_name=str(user.team_name),
            is_active=bool(user.is_active)
        )

    async def get_by_id(self, user_id: str) -> UserResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("user")

        return UserResponse(
            user_id=str(user.user_id),
            username=str(user.username),
            team_name=str(user.team_name),
            is_active=bool(user.is_active)
        )

