from fastapi import FastAPI, HTTPException, Request
from typing import Optional, Dict
import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import pybreaker

app = FastAPI()

# Create a circuit breaker
circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=5,  # Maximum failures before opening the circuit
    reset_timeout=30,  # Time (seconds) before trying again
)

# HTTP client configuration
http_client = httpx.AsyncClient()


# Retry strategy with exponential backoff
@retry(
    stop=stop_after_attempt(3),  # Stop after 3 attempts
    wait=wait_exponential(multiplier=1, min=1, max=10),  # Exponential backoff
    retry=retry_if_exception_type(httpx.RequestError),  # Retry for specific exceptions
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
    if method == "GET":
        response = await http_client.get(url)
    elif method == "POST":
        response = await http_client.post(url, json=payload)
    elif method == "PUT":
        response = await http_client.put(url, json=payload)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()


# Circuit breaker decorator
@circuit_breaker
async def fetch_data_with_circuit_breaker(
    method: str, url: str, payload: Optional[Dict] = None
):
    return await fetch_data_with_retry(method, url, payload)


# FastAPI endpoint
@app.api_route("/external-data", methods=["GET", "POST", "PUT"])
async def handle_external_data(request: Request, payload: Optional[Dict] = None):
    """
    Endpoint to interact with an external service.

    Handles GET, POST, and PUT requests by calling the respective external service.
    """
    try:
        method = request.method
        # Replace this URL with your actual microservice endpoint
        url = "http://example.com/api/data"
        data = await fetch_data_with_circuit_breaker(method, url, payload)
        return {"status": "success", "data": data}
    except pybreaker.CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch data: {str(e)}")
