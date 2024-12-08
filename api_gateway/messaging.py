import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
import httpx
from circuitbreaker import CircuitBreakerError

from rest_interfaces.messaging_interfaces import IConversationList
from main import verify_token_get_user
from retry_circuit_breaker import fetch_data_with_circuit_breaker_messaging


Messaging_router = APIRouter(prefix="/messaging", tags=["messaging"])

MESSAGING_SERVICE_URL = os.getenv("MESSAGING_SERVICE_URL")


@Messaging_router.get("/conversations/{user_id}", response_model=IConversationList)
async def get_conversations(
    user_id: str, user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Mock endpoint to get conversations with your matches.
    Args:
        user_id (uuid): This can be a uuid of a recruiter or a jobseeker.
    """
    if user_id != user["id"]:
        raise HTTPException(
            status_code=403, detail="UserID mismatch: Unauthorized action."
        )
    url = f"{MESSAGING_SERVICE_URL}/conversations/{user_id}"
    try:
        response = await fetch_data_with_circuit_breaker_messaging("GET", url)
        return response.json()
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as exc:
        # Raise an HTTPException with the same status code and error details
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.response.json()
        )
    except Exception as exc:
        # Handle non-HTTP exceptions
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {exc}"
        )
