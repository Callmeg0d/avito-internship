from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.stats_service import StatsService
from app.schemas.stats import StatsResponse

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/assignments", response_model=StatsResponse)
async def get_assignments_stats(
    session: AsyncSession = Depends(get_db)
):
    service = StatsService(session)
    return await service.get_assignments_stats()

