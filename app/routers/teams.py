from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db import get_session
from app.models import Team as TeamModel  # SQLAlchemy model
from app.schemas import Team, TeamCreate  # Pydantic schemas

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=Team, status_code=201)
def create_team(team: TeamCreate, db: Session = Depends(get_session)):
    db_team = db.query(TeamModel).filter(TeamModel.name == team.name).first()
    if db_team:
        raise HTTPException(status_code=400, detail="Team already exists")

    # Create new team
    db_team = TeamModel(name=team.name, description=team.description)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/", response_model=List[Team])
def get_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_session)):
    teams = db.query(TeamModel).offset(skip).limit(limit).all()
    return teams


@router.get("/{team_id}", response_model=Team)
def get_team(team_id: int, db: Session = Depends(get_session)):
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.delete("/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_session)):
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}