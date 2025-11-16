import random
from datetime import datetime
from sqlmodel import Session
from app.models import User, PullRequest
from app.errors import ApiError


def assign_reviewers(session: Session, author: User):
    candidates = (
        session.exec(User)
        .filter(User.team_name == author.team_name, User.is_active == True)
        .all()
    )
    candidates = [c.user_id for c in candidates if c.user_id != author.user_id]

    random.shuffle(candidates)
    return ",".join(candidates[:2])


def reassign_reviewer(session: Session, pr: PullRequest, old_user_id: str):
    if pr.status == "MERGED":
        ApiError.pr_merged()

    reviewers = [r for r in pr.assigned_reviewers.split(",") if r]

    if old_user_id not in reviewers:
        ApiError.not_assigned()

    user = session.get(User, old_user_id)

    team_candidates = (
        session.exec(User)
        .filter(
            User.team_name == user.team_name,
            User.user_id != old_user_id,
            User.is_active == True,
        )
        .all()
    )

    if not team_candidates:
        ApiError.no_candidate()

    new_user = random.choice(team_candidates)

    reviewers = [new_user.user_id if r == old_user_id else r for r in reviewers]
    pr.assigned_reviewers = ",".join(reviewers)
    return new_user.user_id


def merge_pr(pr: PullRequest):
    pr.status = "MERGED"
    if not pr.mergedAt:
        pr.mergedAt = datetime.utcnow()
