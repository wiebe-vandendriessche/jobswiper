import asyncio
from interfaces import IMatchMakingRepository
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from database import Base, engine, MySQL_MatchMakingRepo, SessionLocal


app = FastAPI()
Base.metadata.create_all(bind=engine)


matchmaking_repo: IMatchMakingRepository = MySQL_MatchMakingRepo(
    sessionmaker=SessionLocal
)


# --------------------------------------- THESE ENDPOINT CAN BYPASS APPLICATION LAYER AND GO STRAIGHT TO DATABASE AS THE SERVICE WOULD ADD NO VALUE------------------------------------------------------
@app.get("/recommendations/user/{user_id}")
async def get_user_recommendations(user_id: int):
    try:
        lijst = await matchmaking_repo.find_list_of_recommended_jobs(user_id)
        return lijst
    except Exception as e:
        return HTTPException(501, detail=f"{e}")


# Endpoint for getting recommendations for a job
@app.get("/recommendations/job/{job_id}")
async def get_job_recommendations(job_id: int):
    try:
        lijst = await matchmaking_repo.find_list_of_recommended_jobs(job_id)
        return lijst
    except Exception as e:
        return HTTPException(501, detail=f"{e}")


# -------------------------------------------LIKES/DISLIKES COME IN ASYNCHRONOUS WITH A RABBITMQ BUS --------------------------------------------------------------------------------------
