import asyncio
import json
from interfaces import IMatchMakingRepository, Swipe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, cast
from database import Base, engine, MySQL_MatchMakingRepo, SessionLocal
from application_layer import MatchMakingService


app = FastAPI()
Base.metadata.create_all(bind=engine)


matchmaking_repo: IMatchMakingRepository = MySQL_MatchMakingRepo(
    sessionmaker=SessionLocal
)

matchmaking_service = MatchMakingService(matchmaking_repo)


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


async def process_incoming_message(self, message):

    body = message.body
    if body:
        try:
            swipe = cast(Swipe, json.loads(body))

            if swipe.subject == "user":
                await matchmaking_service.swiped_on_job(
                    swipe.user_id, swipe.job_id, swipe.decision
                )
            elif swipe.subject == "job":
                await matchmaking_service.swiped_on_user(
                    swipe.user_id, swipe.job_id, swipe.decision
                )

        except json.JSONDecodeError as e:
            message.ack()  # bad message
            print(f"Failed to decode JSON: {e}")
        except TypeError as e:
            message.ack()  # bad message
            print(f"Error creating Swipe object: {e}")
        except (
            Exception
        ) as e:  # database exception --> the entity is not processed, procces again so dont ack
            print(f"other error, not acking: {e}")

    message.ack()
