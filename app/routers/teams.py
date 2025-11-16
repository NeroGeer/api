from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db import get_session
from app.models import Team, User
from app.errors import ApiError

router = APIRouter(prefix="/team", tags=["Teams"])


@router.post("/add", status_code=201)
def add_team(team: Team, session: Session = Depends(get_session)):
    existing = session.get(Team, team.team_name)
    if existing:
        ApiError.team_exists()

    session.add(team)

    for member in team.members:
        u = session.get(User, member.user_id)
        if not u:
            session.add(member)
        else:
            u.username = member.username
            u.is_active = member.is_active
            u.team_name = team.team_name

    session.commit()
    return {"team": team}


@router.get("/get")
def get_team(team_name: str, session: Session = Depends(get_session)):
    team = session.get(Team, team_name)
    if not team:
        ApiError.not_found("team not found")
    return team
