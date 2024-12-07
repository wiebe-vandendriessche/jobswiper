import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import httpx
from dataclasses import asdict
from circuitbreaker import CircuitBreakerError
from retry_circuit_breaker import fetch_data_with_circuit_breaker
from rest_interfaces.matching_interfaces import ISwipe, Swipe
from rabbit import PikaPublisher
from main import verify_token_get_user


Matches_router = APIRouter(prefix="/matches", tags=["matches"])

MATCHING_SERVICE_URL = os.getenv("MATCHING_MANAGEMENT_SERVICE_URL")


@Matches_router.get("/recommendations/user/{user_id}")
async def user_recommendations(
    user_id: str, user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Fetch the job recommendations ID's for the User
    """
    # protect the endpoint
    if user["id"] != user_id:
        raise HTTPException(
            status_code=403,
            detail="You requested the recommendations of a user with different user_id",
        )

    url = f"{MATCHING_SERVICE_URL}/recommendations/user/{user_id}"  # Replace with actual URL
    try:
        response = await fetch_data_with_circuit_breaker("GET", url)
        return response.json()  # Return the data if the response is successful
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as http_err:
        # If there's an HTTP error (4xx/5xx), propagate it as a FastAPI HTTPException
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except httpx.RequestError as req_err:
        # For other request errors (e.g., network issues), raise a 500 error
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        # Catch other unforeseen errors and propagate as 500 error
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


# Function to call the job recommendation endpoint using httpx
@Matches_router.get("/recommendations/job/{job_id}")
async def job_recommendations(
    job_id: str, user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Fetch the user recommendations ID's for the Job listing

    """
    url = f"{MATCHING_SERVICE_URL}/recommendations/job/{job_id}"  # Replace with actual URL
    try:
        response = await fetch_data_with_circuit_breaker("GET", url)
        return response.json()  # Return the data if the response is successful
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as http_err:
        # If there's an HTTP error (4xx/5xx), propagate it as a FastAPI HTTPException
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except httpx.RequestError as req_err:
        # For other request errors (e.g., network issues), raise a 500 error
        raise HTTPException(status_code=500, detail=f"Request error: {req_err}")
    except Exception as e:
        # Catch other unforeseen errors and propagate as 500 error
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


# --------------------------------------Publisher endpoint----------------------------------------------------------------
# initialize client on startup
publisher = PikaPublisher(
    os.getenv("BUS_SERVICE"), int(os.getenv("BUS_PORT", 5672)), os.getenv("SWIPES_BUS")
)


@Matches_router.on_event("startup")
async def start_publisher():
    await publisher.initialize()


@Matches_router.post("/swipe/user")
async def user_swipe(
    swipe: ISwipe, user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Swipe right or left on a job listing, based on the boolean in decision

    """

    # protect the endpoint
    if user["id"] != swipe.user_id:
        raise HTTPException(
            status_code=403,
            detail="User_id does not match the user who performed swipe: Unauthorized action.",
        )
    # -----not done yet: check if userid matches swipe userid-----
    try:
        newswipe = Swipe(
            subject="user",
            user_id=swipe.user_id,
            job_id=swipe.job_id,
            decision=swipe.decision,
        )
        await publisher.send_message(asdict(newswipe))
        return {
            "message": "Your swipe is being processed : Put on bus"
        }  # Return the data if the response is successful
    except Exception as e:
        # Catch other unforeseen errors and propagate as 500 error
        raise HTTPException(status_code=501, detail=f"Unexpected error: {e}")


@Matches_router.post("/swipe/job")
async def job_swipe(
    swipe: ISwipe, user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Swipe right or left on a job listing, based on the boolean in decision

    """
    # -----not done yet: check if userid matches swipe userid-----
    try:
        newswipe = Swipe(
            subject="job",
            user_id=swipe.user_id,
            job_id=swipe.job_id,
            decision=swipe.decision,
        )
        await publisher.send_message(asdict(newswipe))
        return {
            "message": "Your swipe is being processed : Put on bus"
        }  # Return the data if the response is successful
    except Exception as e:
        # Catch other unforeseen errors and propagate as 500 error
        raise HTTPException(status_code=501, detail=f"Unexpected error: {e}")
