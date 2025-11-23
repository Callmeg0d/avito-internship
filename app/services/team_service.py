from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import random

from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository
from app.models.team import Team
from app.models.user import User
from app.schemas.team import TeamCreate, TeamResponse, TeamMember
from app.exceptions import TeamExistsException, NotFoundException


class TeamService:
    def __init__(self, session: AsyncSession):
        self.team_repo = TeamRepository(session)
        self.user_repo = UserRepository(session)

    async def create_team(self, team_data: TeamCreate) -> TeamResponse:
        if await self.team_repo.exists(team_data.team_name):
            raise TeamExistsException()

        team = Team(team_name=team_data.team_name)
        await self.team_repo.create(team)

        members = []
        for member_data in team_data.members:
            user = User(
                user_id=member_data.user_id,
                username=member_data.username,
                is_active=member_data.is_active,
                team_name=team_data.team_name
            )
            await self.user_repo.create_or_update(user)
            members.append(TeamMember(
                user_id=str(user.user_id),
                username=str(user.username),
                is_active=bool(user.is_active)
            ))

        return TeamResponse(team_name=team_data.team_name, members=members)

    async def get_team(self, team_name: str) -> TeamResponse:
        team = await self.team_repo.get_by_name(team_name)
        if not team:
            raise NotFoundException("team")

        members = [
            TeamMember(
                user_id=str(member.user_id),
                username=str(member.username),
                is_active=bool(member.is_active)
            )
            for member in team.members
        ]

        return TeamResponse(team_name=str(team.team_name), members=members)

    async def get_active_reviewers(self, team_name: str, exclude_user_id: str, count: int = 2) -> List[str]:
        candidates = await self.user_repo.get_active_by_team(team_name, exclude_user_id)
        random.shuffle(candidates)
        return [str(user.user_id) for user in candidates[:count]]

