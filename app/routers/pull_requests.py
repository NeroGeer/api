from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.models import PullRequest, User
from app.logic import assign_reviewers, reassign_reviewer, merge_pr
from app.errors import ApiError
from datetime import datetime

router = APIRouter(prefix="/pullRequest", tags=["PullRequests"])


@router.post("/create", status_code=201)
def create_pr(payload: dict, session: Session = Depends(get_session)):
    pr_id = payload["pull_request_id"]
    if session.get(PullRequest, pr_id):
        ApiError.pr_exists()

    author = session.get(User, payload["author_id"])
    if not author:
        ApiError.not_found("author not found")

    reviewers = assign_reviewers(session, author)

    pr = PullRequest(
        pull_request_id=pr_id,
        pull_request_name=payload["pull_request_name"],
        author_id=payload["author_id"],
        status="OPEN",
        assigned_reviewers=reviewers,
        createdAt=datetime.utcnow(),
    )
    session.add(pr)
    session.commit()
    session.refresh(pr)
    return {"pr": pr}


@router.post("/merge")
def merge(payload: dict, session: Session = Depends(get_session)):
    pr = session.get(PullRequest, payload["pull_request_id"])
    if not pr:
        ApiError.not_found("PR not found")

    merge_pr(pr)
    session.commit()
    return {"pr": pr}


@router.post("/reassign")
def reassign(payload: dict, session: Session = Depends(get_session)):
    pr = session.get(PullRequest, payload["pull_request_id"])
    if not pr:
        ApiError.not_found("PR not found")

    replaced = reassign_reviewer(session, pr, payload["old_user_id"])
    session.commit()
    return {"pr": pr, "replaced_by": replaced}
