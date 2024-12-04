import asyncio
from matching.swipes import on_message
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import aio_pika


app = FastAPI()

# MongoDB connection string
MONGO_DETAILS = "mongodb://root:example@mongodb:27017/recommendation_db"
RABBITMQ_URL = "amqp://guest:guest@localhost/"


client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.recommendation_db

# Collections
user_recommendations = database.get_collection("user_recommendations")
job_recommendations = database.get_collection("job_recommendations")


async def consume_rabbitmq():
    """Asynchronous function to consume messages from RabbitMQ queue."""
    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        # Declare the queue
        queue = await channel.declare_queue("swipes_queue", durable=True)
        # Start consuming messages asynchronously
        await queue.consume(on_message)
        print("RabbitMQ consumer is running.")


# Startup
asyncio.create_task(consume_rabbitmq())


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
