from fastapi import FastAPI
from sqlmodel import SQLModel
from app.routers import teams, users, pull_requests, health

from app.db import engine


app = FastAPI()


SQLModel.metadata.create_all(engine)


app.include_router(teams.router)
app.include_router(users.router)
app.include_router(pull_requests.router)
app.include_router(health.router)