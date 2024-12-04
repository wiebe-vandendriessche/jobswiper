import asyncio
from matching.swipes import on_message
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pika


app = FastAPI()


app = FastAPI()


# Pydantic Models
class UserRecommendation(BaseModel):
    recommended_jobs: List[str]


class JobRecommendation(BaseModel):
    recommended_users: List[str]


# Endpoint for getting recommendations for a user
@app.get("/recommendations/user/{user_id}", response_model=UserRecommendation)
async def get_user_recommendations(user_id: str):
    user = await user_recommendations.find_one({"_id": user_id})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRecommendation(recommended_jobs=user["recommended_jobs"])


# Endpoint for getting recommendations for a job
@app.get("/recommendations/job/{job_id}", response_model=JobRecommendation)
async def get_job_recommendations(job_id: str):
    job = await job_recommendations.find_one({"_id": job_id})
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobRecommendation(recommended_users=job["recommended_users"])
