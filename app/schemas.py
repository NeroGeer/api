from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base schemas
class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # This replaces `orm_mode = True` in Pydantic v2


# User schemas
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Pull Request schemas
class PRBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str


class PRCreate(PRBase):
    team_id: int
    author_id: int


class PR(PRBase):
    id: int
    team_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
