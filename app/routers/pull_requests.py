from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.pull_request_service import PullRequestService
from app.schemas.pull_request import (
    PullRequestCreate,
    PullRequestMerge,
    PullRequestReassign,
    PullRequestReassignResponse
)

router = APIRouter(prefix="/pullRequest", tags=["PullRequests"])


@router.post("/create", response_model=dict, status_code=201)
async def create_pr(
    pr_data: PullRequestCreate,
    session: AsyncSession = Depends(get_db)
):
    service = PullRequestService(session)
    pr = await service.create_pr(pr_data)
    await session.commit()
    return {"pr": pr.model_dump()}


@router.post("/merge", response_model=dict)
async def merge_pr(
    merge_data: PullRequestMerge,
    session: AsyncSession = Depends(get_db)
):
    service = PullRequestService(session)
    pr = await service.merge_pr(merge_data)
    await session.commit()
    return {"pr": pr.model_dump()}


@router.post("/reassign", response_model=PullRequestReassignResponse)
async def reassign_reviewer(
    reassign_data: PullRequestReassign,
    session: AsyncSession = Depends(get_db)
):
    service = PullRequestService(session)
    result = await service.reassign_reviewer(reassign_data)
    await session.commit()
    return result

