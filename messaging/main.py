import asyncio
import json
import logging
import os
from typing import List
import aio_pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from consumer import PikaConsumer

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Recommendation(BaseModel):
    user_id: str
    job_id: str
    recruiter_id: str
    user_likes: bool
    recruiter_likes: bool


class Match(BaseModel):
    jobseeker_id: str
    job_id: str


class IConversationList(BaseModel):
    is_jobseeker: bool | None
    matches: List[Match]


app = FastAPI()

my_database = []


test = {
    "user_id": "yappa",
    "job_id": "jobyappa",
    "recruiter_id": "recruiteryappe",
    "user_likes": True,
    "recruiter_likes": True,
}


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    consumer = PikaConsumer(
        host=os.getenv("BUS_SERVICE"),
        port=int(os.getenv("BUS_PORT", 5672)),
        queue_name=os.getenv("MATCH_BUS"),
        consumer_function=process_incoming_message,
    )
    task = loop.create_task(consumer.consume(loop))
    await task


@app.get("/conversations/{user_id}", response_model=IConversationList)
async def get_conversations_user(user_id: str):
    """
    Mock endpoint to get conversations with your matches.
    Args:
        user_id (uuid): This can be a uuid of a recruiter or a jobseeker.
    """
    try:
        response = IConversationList(is_jobseeker=True, matches=[])
        type = None
        for items in my_database:  # fake database traversel
            if type is None:
                if items.user_id == user_id:
                    type = True  # it is a jobseeker
                if items.recruiter_id == user_id:
                    type = False  # it is a recruiter
            if type == True and items.user_id == user_id:
                response.matches.append(
                    Match(jobseeker_id=items.user_id, job_id=items.job_id)
                )
            if type == False and items.recruiter_id == user_id:
                response.matches.append(
                    Match(jobseeker_id=items.user_id, job_id=items.job_id)
                )
        response.is_jobseeker = type
        return response
    except Exception as e:
        return HTTPException(status_code=500, detail=f"Messaging service:{e}")


async def process_incoming_message(message: aio_pika.IncomingMessage):

    body = message.body
    try:
        if body:
            data = json.loads(body)
            match = Recommendation(**data)
            logger.info(f"MESSAGE RECIEVED:{match}")
            my_database.append(match)
        await message.ack()

    except json.JSONDecodeError as e:
        await message.ack()  # bad message
        logger.warning(f"Failed to decode JSON: {e}")
    except TypeError as e:
        await message.ack()  # bad message
        logger.warning(f"Error creating Match object: {e}")
    except NameError as e:
        await message.ack()  # bad message
        logger.warning(f"404:{e}")

    except (
        Exception
    ) as e:  # database exception --> the entity is not processed, procces again so dont ack
        logger.warning(f"other error, not acking: {e}")
