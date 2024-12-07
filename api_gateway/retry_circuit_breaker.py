import logging
from typing import Optional, Dict
from fastapi import HTTPException
import httpx
from tenacity import (
    after_log,
    before_log,
    retry,
    RetryError,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    wait_random_exponential,
)
from circuitbreaker import circuit


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------- combine circuitbreaker with exponential backoff retries -------------------------------------------------------
# Create a circuit breaker


# Circuit breaker decorator
@circuit(
    failure_threshold=3, recovery_timeout=30, expected_exception=RetryError
)  # this is a threadwide circuitbreaker -> three consecutive fails-->open circuit
async def fetch_data_with_circuit_breaker(
    method: str, url: str, payload: Optional[Dict] = None
):
    try:
        return await fetch_data_with_retry(method, url, payload)
    except httpx.HTTPStatusError as exc:
        # Raise an HTTPException with the same status code and error details -_> will be ignored by circuitbraker
        raise HTTPException(
            status_code=exc.response.status_code, detail=exc.response.json()
        )


# -------------------------------Retry strategy with exponential backoff----------------------------------------------
"""
Attempt 1: Wait randomly between 0 and 2^1 = 2 seconds before retrying.
Attempt 2: Wait randomly between 0 and 2^2 = 4 seconds before retrying.
Attempt 3: Wait randomly between 0 and 2^3 = 8 seconds before retrying.
Attempt 4: Wait randomly between 0 and 2^4 = 16 seconds before retrying.
Attempt 5: Wait randomly between 0 and 2^5 = 32 seconds before retrying
"""


@retry(
    wait=wait_random_exponential(
        multiplier=1, max=30
    ),  # Random wait, capped at 60 seconds
    stop=stop_after_attempt(4),
    retry=retry_if_exception_type(
        httpx.RequestError
    ),  # Retry only for when request is not processed --> service down (connectionerror, readTimeout, Write Error,...)
    after=after_log(logger, logging.INFO),  # Log after retry
)
async def fetch_data_with_retry(method: str, url: str, payload: Optional[Dict] = None):
    """
    Handles GET, POST, and PUT requests with retries.

    Args:
        method (str): HTTP method ('GET', 'POST', 'PUT').
        url (str): URL to make the request to.
        payload (Optional[Dict]): Payload for POST or PUT requests.

    Returns:
        JSON response from the external service.
    """
    async with httpx.AsyncClient() as http_client:
        if method == "GET":
            response = await http_client.get(url)
        elif method == "POST":
            response = await http_client.post(url, json=payload)
        elif method == "PUT":
            response = await http_client.put(url, json=payload)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()  # Raise exception for HTTP errors
        return response
