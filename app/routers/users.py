from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.user_service import UserService
from app.services.pull_request_service import PullRequestService
from app.schemas.user import UserActivityUpdate
from app.schemas.pull_request import UserReviewResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/setIsActive", response_model=dict)
async def set_user_activity(
    data: UserActivityUpdate,
    session: AsyncSession = Depends(get_db)
):
    service = UserService(session)
    user = await service.set_activity(data)
    await session.commit()
    return {"user": user.model_dump()}


@router.get("/getReview", response_model=UserReviewResponse)
async def get_user_reviews(
    user_id: str = Query(..., alias="user_id"),
    session: AsyncSession = Depends(get_db)
):
    service = PullRequestService(session)
    return await service.get_user_reviews(user_id)

