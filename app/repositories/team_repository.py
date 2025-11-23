from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional

from app.models.team import Team


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, team_name: str) -> Optional[Team]:
        result = await self.session.execute(
            select(Team)
            .options(selectinload(Team.members))
            .where(Team.team_name == team_name)
        )
        return result.scalar_one_or_none()

    async def create(self, team: Team) -> Team:
        self.session.add(team)
        await self.session.flush()
        return team

    async def exists(self, team_name: str) -> bool:
        team = await self.get_by_name(team_name)
        return team is not None

