from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# MongoDB connection string
MONGO_DETAILS = "mongodb://root:example@mongodb:27017/recommendation_db"

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.recommendation_db

# Collections
user_recommendations = database.get_collection("user_recommendations")
job_recommendations = database.get_collection("job_recommendations")

