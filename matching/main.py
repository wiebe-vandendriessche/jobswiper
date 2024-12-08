import asyncio
import json
import logging
import os

import aio_pika
from interfaces import IMatchMakingRepository, Swipe
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, cast
from database import Base, engine, MySQL_MatchMakingRepo, SessionLocal
from application_layer import MatchMakingService
from rabbit import PikaConsumer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI()
Base.metadata.create_all(bind=engine)


matchmaking_repo: IMatchMakingRepository = MySQL_MatchMakingRepo(
    sessionmaker=SessionLocal
)

matchmaking_service = MatchMakingService(matchmaking_repo)


# ------------------------------------------SETUP CONSUMER ASYNCHRONOUSLY--------------------
@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    consumer = PikaConsumer(
        host=os.getenv("BUS_SERVICE"),
        port=int(os.getenv("BUS_PORT", 5672)),
        queue_name=os.getenv("SWIPES_BUS"),
        consumer_function=process_incoming_message,
    )
    task = loop.create_task(consumer.consume(loop))
    await task


# --------------------------------------- THESE ENDPOINT CAN BYPASS APPLICATION LAYER AND GO STRAIGHT TO DATABASE AS THE SERVICE WOULD ADD NO VALUE------------------------------------------------------
@app.get("/recommendations/user/{user_id}")
async def get_user_recommendations(user_id: str):
    try:
        lijst = await matchmaking_repo.find_list_of_recommended_jobs(user_id)
        return lijst
    except Exception as e:
        return HTTPException(501, detail=f"{e}")


# Endpoint for getting recommendations for a job
@app.get("/recommendations/job/{job_id}")
async def get_job_recommendations(job_id: str):
    try:
        lijst = await matchmaking_repo.find_list_of_recommended_users(job_id)
        return lijst
    except Exception as e:
        return HTTPException(501, detail=f"{e}")


# -------------------------------------------LIKES/DISLIKES COME IN ASYNCHRONOUS WITH A RABBITMQ BUS --------------------------------------------------------------------------------------


async def process_incoming_message(message: aio_pika.IncomingMessage):

    body = message.body
    try:
        if body:
            data = json.loads(body)
            swipe = Swipe(**data)
            logger.info(f"MESSAGE RECIEVED:{swipe}")
            if swipe.subject == "user":
                await matchmaking_service.swiped_on_job(
                    swipe.user_id, swipe.job_id, swipe.decision
                )
            elif swipe.subject == "job":
                await matchmaking_service.swiped_on_user(
                    swipe.user_id, swipe.job_id, swipe.decision
                )
        await message.ack()

    except json.JSONDecodeError as e:
        await message.ack()  # bad message
        logger.warning(f"Failed to decode JSON: {e}")
    except TypeError as e:
        await message.ack()  # bad message
        logger.warning(f"Error creating Swipe object: {e}")
    except NameError as e:
        await message.ack()  # bad message
        logger.warning(f"404:{e}")

    except (
        Exception
    ) as e:  # database exception --> the entity is not processed, procces again so dont ack
        logger.warning(f"other error, not acking: {e}")
