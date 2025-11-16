from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from models import PRStatus


class TeamMember(BaseModel):
    user_id: str
    username: str
    is_active: bool


class TeamBase(BaseModel):
    team_name: str
    members: List[TeamMember]


class TeamResponse(BaseModel):
    team: TeamBase


class UserResponse(BaseModel):
    user_id: str
    username: str
    team_name: str
    is_active: bool


class PullRequestShort(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PRStatus


class PullRequestBase(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PRStatus
    assigned_reviewers: List[str]
    createdAt: Optional[datetime] = None
    mergedAt: Optional[datetime] = None


class PullRequestCreate(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str


class PullRequestMerge(BaseModel):
    pull_request_id: str


class PullRequestReassign(BaseModel):
    pull_request_id: str
    old_user_id: str


class PullRequestResponse(BaseModel):
    pr: PullRequestBase


class PullRequestReassignResponse(BaseModel):
    pr: PullRequestBase
    replaced_by: str


class UserReviewList(BaseModel):
    user_id: str
    pull_requests: List[PullRequestShort]


class ErrorItem(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorItem
