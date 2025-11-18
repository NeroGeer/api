from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_session
from app.models import PullRequest, User, Team
from app.logic import assign_reviewers, reassign_reviewer, merge_pr
from app.errors import ApiError
from datetime import datetime

router = APIRouter(prefix="/pullRequest", tags=["PullRequests"])


@router.post("/create", status_code=201)
def create_pr(payload: dict, session: Session = Depends(get_session)):
    # Проверяем существование PR по ID
    existing_pr = session.get(PullRequest, payload.get("id"))
    if existing_pr:
        raise ApiError.pr_exists()

    author = session.get(User, payload.get("author_id"))
    if not author:
        raise ApiError.not_found("author not found")

    team = session.get(Team, payload.get("team_id"))
    if not team:
        raise ApiError.not_found("team not found")

    reviewers = assign_reviewers(session, author)

    pr = PullRequest(
        title=payload["title"],
        description=payload.get("description"),
        status="open",
        team_id=payload["team_id"],
        author_id=payload["author_id"],
        created_at=datetime.utcnow(),
    )
    session.add(pr)
    session.commit()
    session.refresh(pr)
    return {"pr": pr}


@router.post("/merge")
def merge(payload: dict, session: Session = Depends(get_session)):
    pr = session.get(PullRequest, payload["pull_request_id"])
    if not pr:
        raise ApiError.not_found("PR not found")

    merge_pr(pr)
    session.commit()
    session.refresh(pr)
    return {"pr": pr}


@router.post("/reassign")
def reassign(payload: dict, session: Session = Depends(get_session)):
    pr = session.get(PullRequest, payload["pull_request_id"])
    if not pr:
        raise ApiError.not_found("PR not found")

    replaced = reassign_reviewer(session, pr, payload["old_user_id"])
    session.commit()
    session.refresh(pr)
    return {"pr": pr, "replaced_by": replaced}
