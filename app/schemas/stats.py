from pydantic import BaseModel
from typing import List


class UserStats(BaseModel):
    user_id: str
    username: str
    assignments_count: int


class StatsResponse(BaseModel):
    total_assignments: int
    users: List[UserStats]

