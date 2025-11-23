from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PullRequestCreate(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str


class PullRequestResponse(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: str
    assigned_reviewers: List[str]
    createdAt: Optional[datetime] = None
    mergedAt: Optional[datetime] = None


class PullRequestShort(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: str


class PullRequestMerge(BaseModel):
    pull_request_id: str


class PullRequestReassign(BaseModel):
    pull_request_id: str
    old_user_id: str


class PullRequestReassignResponse(BaseModel):
    pr: PullRequestResponse
    replaced_by: str


class UserReviewResponse(BaseModel):
    user_id: str
    pull_requests: List[PullRequestShort]

