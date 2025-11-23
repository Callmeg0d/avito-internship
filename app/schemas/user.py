from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: str
    username: str
    team_name: str
    is_active: bool


class UserActivityUpdate(BaseModel):
    user_id: str
    is_active: bool

