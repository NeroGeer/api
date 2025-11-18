from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_session
from app.models import User, PullRequest, Team
from app.errors import ApiError

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/setIsActive")
def set_is_active(payload: dict, session: Session = Depends(get_session)):
    user = session.get(User, payload["user_id"])
    if not user:
        raise ApiError.not_found("user not found")

    user.is_active = payload["is_active"]
    session.commit()
    session.refresh(user)
    return {"user": user}


@router.get("/getReview")
def get_reviews(user_id: int, session: Session = Depends(get_session)):
    # Получаем пользователя
    user = session.get(User, user_id)
    if not user:
        raise ApiError.not_found("user not found")

    stmt = select(PullRequest).where(PullRequest.author_id == user_id)
    prs = session.execute(stmt).scalars().all()

    result = [
        {
            "id": pr.id,
            "title": pr.title,
            "description": pr.description,
            "status": pr.status,
            "team_id": pr.team_id,
            "author_id": pr.author_id,
            "created_at": pr.created_at,
            "updated_at": pr.updated_at,
        }
        for pr in prs
    ]

    return {"user_id": user_id, "pull_requests": result}