from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.team_service import TeamService
from app.schemas.team import TeamCreate, TeamResponse

router = APIRouter(prefix="/team", tags=["Teams"])


@router.post("/add", response_model=dict, status_code=201)
async def create_team(
    team_data: TeamCreate,
    session: AsyncSession = Depends(get_db)
):
    service = TeamService(session)
    team = await service.create_team(team_data)
    await session.commit()
    return {"team": team.model_dump()}


@router.get("/get", response_model=TeamResponse)
async def get_team(
    team_name: str = Query(..., alias="team_name"),
    session: AsyncSession = Depends(get_db)
):
    service = TeamService(session)
    return await service.get_team(team_name)

