from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import random

from app.repositories.pull_request_repository import PullRequestRepository
from app.repositories.user_repository import UserRepository
from app.repositories.team_repository import TeamRepository
from app.models.pull_request import PullRequest, PRStatus
from app.schemas.pull_request import (
    PullRequestCreate,
    PullRequestResponse,
    PullRequestShort,
    PullRequestMerge,
    PullRequestReassign,
    PullRequestReassignResponse,
    UserReviewResponse
)
from app.exceptions import (
    PRExistsException,
    PRMergedException,
    NotAssignedException,
    NoCandidateException,
    NotFoundException
)


class PullRequestService:
    def __init__(self, session: AsyncSession):
        self.pr_repo = PullRequestRepository(session)
        self.user_repo = UserRepository(session)
        self.team_repo = TeamRepository(session)

    async def create_pr(self, pr_data: PullRequestCreate) -> PullRequestResponse:
        if await self.pr_repo.exists(pr_data.pull_request_id):
            raise PRExistsException()

        author = await self.user_repo.get_by_id(pr_data.author_id)
        if not author:
            raise NotFoundException("author")

        team = await self.team_repo.get_by_name(str(author.team_name))
        if not team:
            raise NotFoundException("team")

        pr = PullRequest(
            pull_request_id=pr_data.pull_request_id,
            pull_request_name=pr_data.pull_request_name,
            author_id=pr_data.author_id,
            status=PRStatus.OPEN,
            created_at=datetime.utcnow()
        )
        await self.pr_repo.create(pr)

        # Назначаем до 2 активных ревьюверов из команды автора
        candidates = await self.user_repo.get_active_by_team(str(author.team_name), pr_data.author_id)
        random.shuffle(candidates)
        reviewers = candidates[:2]

        for reviewer in reviewers:
            await self.pr_repo.add_reviewer(str(pr.pull_request_id), str(reviewer.user_id))

        reviewer_ids = [str(r.user_id) for r in reviewers]
        return PullRequestResponse(
            pull_request_id=str(pr.pull_request_id),
            pull_request_name=str(pr.pull_request_name),
            author_id=str(pr.author_id),
            status=str(pr.status.value),
            assigned_reviewers=reviewer_ids,
            createdAt=pr.created_at,
            mergedAt=pr.merged_at
        )

    async def merge_pr(self, merge_data: PullRequestMerge) -> PullRequestResponse:
        pr = await self.pr_repo.merge(merge_data.pull_request_id)
        if not pr:
            raise NotFoundException("pull request")

        reviewer_ids = await self.pr_repo.get_reviewers(str(pr.pull_request_id))
        return PullRequestResponse(
            pull_request_id=str(pr.pull_request_id),
            pull_request_name=str(pr.pull_request_name),
            author_id=str(pr.author_id),
            status=str(pr.status.value),
            assigned_reviewers=[str(rid) for rid in reviewer_ids],
            createdAt=pr.created_at,
            mergedAt=pr.merged_at
        )

    async def reassign_reviewer(self, reassign_data: PullRequestReassign) -> PullRequestReassignResponse:
        pr = await self.pr_repo.get_by_id(reassign_data.pull_request_id)
        if not pr:
            raise NotFoundException("pull request")

        if pr.status == PRStatus.MERGED:
            raise PRMergedException()

        reviewer_ids = await self.pr_repo.get_reviewers(str(pr.pull_request_id))
        if reassign_data.old_user_id not in reviewer_ids:
            raise NotAssignedException()

        old_reviewer = await self.user_repo.get_by_id(reassign_data.old_user_id)
        if not old_reviewer:
            raise NotFoundException("reviewer")

        # Ищем активных кандидатов из команды заменяемого ревьювера
        candidates = await self.user_repo.get_active_by_team(
            str(old_reviewer.team_name),
            exclude_user_id=reassign_data.old_user_id
        )

        # Исключаем уже назначенных ревьюверов
        candidate_ids = {str(c.user_id) for c in candidates}
        candidate_ids.discard(reassign_data.old_user_id)
        for rid in reviewer_ids:
            candidate_ids.discard(str(rid))

        if not candidate_ids:
            raise NoCandidateException()

        new_reviewer_id = random.choice(list(candidate_ids))

        await self.pr_repo.remove_reviewer(str(pr.pull_request_id), reassign_data.old_user_id)
        await self.pr_repo.add_reviewer(str(pr.pull_request_id), new_reviewer_id)

        updated_reviewer_ids = await self.pr_repo.get_reviewers(str(pr.pull_request_id))
        return PullRequestReassignResponse(
            pr=PullRequestResponse(
                pull_request_id=str(pr.pull_request_id),
                pull_request_name=str(pr.pull_request_name),
                author_id=str(pr.author_id),
                status=str(pr.status.value),
                assigned_reviewers=[str(rid) for rid in updated_reviewer_ids],
                createdAt=pr.created_at,
                mergedAt=pr.merged_at
            ),
            replaced_by=new_reviewer_id
        )

    async def get_user_reviews(self, user_id: str) -> UserReviewResponse:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundException("user")

        prs = await self.pr_repo.get_by_reviewer(user_id)
        return UserReviewResponse(
            user_id=user_id,
            pull_requests=[
                PullRequestShort(
                    pull_request_id=str(pr.pull_request_id),
                    pull_request_name=str(pr.pull_request_name),
                    author_id=str(pr.author_id),
                    status=str(pr.status.value)
                )
                for pr in prs
            ]
        )
