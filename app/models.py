from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, DeclarativeBase

import enum


class Base(DeclarativeBase):
    pass


class PRStatus(str, enum.Enum):
    OPEN = "OPEN"
    MERGED = "MERGED"


class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    team_name = Column(String, ForeignKey("teams.team_name", ondelete="SET NULL"))
    is_active = Column(Boolean, default=True, nullable=False)

    team = relationship("Team", back_populates="members")
    reviewer_in = relationship("PullRequestReviewer", back_populates="reviewer")


class Team(Base):
    __tablename__ = "teams"

    team_name = Column(String, primary_key=True)
    members = relationship("User", back_populates="team", cascade="all, delete-orphan")


class PullRequest(Base):
    __tablename__ = "pull_requests"


    pull_request_id = Column(String, primary_key=True)
    pull_request_name = Column(String, nullable=False)
    author_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"))
    status = Column(Enum(PRStatus), default=PRStatus.OPEN, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    mergedAt = Column(DateTime, nullable=True)

    author = relationship("User")
    reviewers = relationship("PullRequestReviewer", back_populates="pull_request", cascade="all, delete-orphan")


class PullRequestReviewer(Base):
    __tablename__ = "pull_request_reviewers"

    pull_request_id = Column(String, ForeignKey("pull_requests.pull_request_id", ondelete="CASCADE"), primary_key=True)
    reviewer_id = Column(String, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    pull_request = relationship("PullRequest", back_populates="reviewers")
    reviewer = relationship("User", back_populates="reviewer_in")

