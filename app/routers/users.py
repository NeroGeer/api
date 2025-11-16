from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db import get_session
from app.models import User, PullRequest
from app.errors import ApiError

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/setIsActive")
def set_is_active(payload: dict, session: Session = Depends(get_session)):
    user = session.get(User, payload["user_id"])
    if not user:
        ApiError.not_found("user not found")

    user.is_active = payload["is_active"]
    session.commit()
    return {"user": user}


@router.get("/getReview")
def get_reviews(user_id: str, session: Session = Depends(get_session)):
    prs = session.exec(select(PullRequest)).all()
    result = [
        {
            "pull_request_id": pr.pull_request_id,
            "pull_request_name": pr.pull_request_name,
            "author_id": pr.author_id,
            "status": pr.status,
        }
        for pr in prs
        if user_id in pr.assigned_reviewers.split(",")
    ]

    return {"user_id": user_id, "pull_requests": result}
