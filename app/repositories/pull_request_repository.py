from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List
from datetime import datetime

from app.models.pull_request import PullRequest, PullRequestReviewer, PRStatus


class PullRequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, pull_request_id: str) -> Optional[PullRequest]:
        result = await self.session.execute(
            select(PullRequest).where(PullRequest.pull_request_id == pull_request_id)
        )
        return result.scalar_one_or_none()

    async def create(self, pr: PullRequest) -> PullRequest:
        self.session.add(pr)
        await self.session.flush()
        return pr

    async def exists(self, pull_request_id: str) -> bool:
        pr = await self.get_by_id(pull_request_id)
        return pr is not None

    async def merge(self, pull_request_id: str) -> Optional[PullRequest]:
        pr = await self.get_by_id(pull_request_id)
        if pr and pr.status != PRStatus.MERGED:
            pr.status = PRStatus.MERGED  # type: ignore[assignment]
            if pr.merged_at is None:
                pr.merged_at = datetime.utcnow()  # type: ignore[assignment]
            await self.session.flush()
        return pr

    async def add_reviewer(self, pull_request_id: str, reviewer_id: str) -> PullRequestReviewer:
        reviewer = PullRequestReviewer(
            id=f"{pull_request_id}_{reviewer_id}",
            pull_request_id=pull_request_id,
            reviewer_id=reviewer_id
        )
        self.session.add(reviewer)
        await self.session.flush()
        return reviewer

    async def remove_reviewer(self, pull_request_id: str, reviewer_id: str) -> bool:
        result = await self.session.execute(
            select(PullRequestReviewer).where(
                and_(
                    PullRequestReviewer.pull_request_id == pull_request_id,
                    PullRequestReviewer.reviewer_id == reviewer_id
                )
            )
        )
        reviewer = result.scalar_one_or_none()
        if reviewer:
            await self.session.delete(reviewer)
            await self.session.flush()
            return True
        return False

    async def get_reviewers(self, pull_request_id: str) -> List[str]:
        result = await self.session.execute(
            select(PullRequestReviewer.reviewer_id).where(
                PullRequestReviewer.pull_request_id == pull_request_id
            )
        )
        return list(result.scalars().all())

    async def get_by_reviewer(self, reviewer_id: str) -> List[PullRequest]:
        result = await self.session.execute(
            select(PullRequest)
            .join(
                PullRequestReviewer,
                PullRequest.pull_request_id == PullRequestReviewer.pull_request_id
            )
            .where(PullRequestReviewer.reviewer_id == reviewer_id)
            .order_by(PullRequest.created_at.desc())
        )
        return list(result.scalars().all())

