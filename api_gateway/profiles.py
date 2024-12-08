import json
import os
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
import httpx
from circuitbreaker import CircuitBreakerError

from retry_circuit_breaker import fetch_data_with_circuit_breaker
from caching import cache_profile, get_profile, remove_profile_cache
from rest_interfaces.profile_interfaces import IJobSeeker, IRecruiter, IUserProfile, JobSeekerUpdateRequest, JobseekerPreview, RecruiterUpdateRequest
from main import verify_token_get_user


Profile_router = APIRouter(prefix="/profile", tags=["profiles"])

PROFILE_MANAGEMENT_SERVICE_URL = os.getenv("PROFILE_MANAGEMENT_SERVICE_URL")


@Profile_router.post("/")
async def profile_create(
    user: Annotated[dict, Depends(verify_token_get_user)],
    data: Union[IJobSeeker, IRecruiter],
):
    """
    Send a POST request to create a profile.

    Args:
        user (dict): The authenticated user's data obtained from the token.
        data (IUserProfile): The details of the user profile to create.

    Returns:
        dict: The response from the profile management service.
    """
    if user["username"] != data.username:
        raise HTTPException(
            status_code=403, detail="Username mismatch: Unauthorized action."
        )
    
    data.id=user["id"] #zodat dezelfde id heeft over verschillende databases
    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/accounts"
    try:
        response= await fetch_data_with_circuit_breaker("POST",url,data.model_dump())
        return response.json()  # Return the response from the external service
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as exc:
        # Raise an HTTP exception with details from the external service
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"Error from profile management service: {exc.response.text}",
        )
    except Exception as exc:
        # Catch all other exceptions and raise as 500 Internal Server Error
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(exc)}"
        )
@Profile_router.get("/{user_id}/preview",response_model=JobseekerPreview)
async def profile_get_preview(
    user_id:str,
    user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Get the details of a job seeker account by uuid.
    - userid: The uuid of the account to fetch.
    All users can get preview of other jobseeker if logged in.
    """
    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/accounts/{user_id}/preview"
    try:
        response = await fetch_data_with_circuit_breaker("GET",url)
        return response.json()
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as exc:
        # Raise an HTTPException with the same status code and error details
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json()
        )
    except Exception as exc:
        # Handle non-HTTP exceptions
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {exc}"
        )

@Profile_router.get("/{username}",response_model=Union[IJobSeeker,IRecruiter])
async def profile_get(
    username:str,
    user: Annotated[dict, Depends(verify_token_get_user)]
):
    """
    Fetch the details of a job seeker or recruiter account by username.
    """
    if(username!=user["username"]):
        raise HTTPException(
            status_code=403, detail="Username mismatch: Unauthorized action."
        )        
    #check in cache
    cache=get_profile(user["username"])
    if cache:
        return json.loads(cache)
    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/accounts/{user["username"]}"
    try:
        response = await fetch_data_with_circuit_breaker("GET",url)
        cache_profile(user["username"],response.text)
        return response.json()
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as exc:
        # Raise an HTTPException with the same status code and error details
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json()
        )
    except Exception as exc:
        # Handle non-HTTP exceptions
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {exc}"
        )
        
@Profile_router.put("/jobseeker/{username}")
async def update_job_seeker(username: str, update_data: JobSeekerUpdateRequest,user:Annotated[dict, Depends(verify_token_get_user)]):
    """
    Update the details of a job seeker by username.
    """
    if(username!=user["username"]):
        raise HTTPException(
            status_code=403, detail="Username mismatch: Unauthorized action."
        )      
    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/job_seeker/{username}"
    try:
        response = await fetch_data_with_circuit_breaker("PUT",url,update_data.model_dump())
        #clear the original cache because you updated the person
        remove_profile_cache(username)
        return response.json()
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as exc:
        # Raise an HTTPException with the same status code and error details
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json() 
        )
    except Exception as exc:
        # Handle non-HTTP exceptions
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while fetching the profile.: {exc}"
        )
        
@Profile_router.put("/recruiter/{username}")
async def update_recruiter(username:str,update_data:RecruiterUpdateRequest,user:Annotated[dict, Depends(verify_token_get_user)]):
    """
    Update the details of a recruiter by username.
    """
    if(username!=user["username"]):
        raise HTTPException(
            status_code=403, detail="Username mismatch: Unauthorized action."
        )      
    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/recruiter/{username}"
    try:
        response = await fetch_data_with_circuit_breaker("PUT",url,update_data.model_dump())
        #remove from cache
        remove_profile_cache(username)
        return response.json()
    except CircuitBreakerError:
        raise HTTPException(
            status_code=503, detail="Service unavailable (circuit open)"
        )
    except httpx.HTTPStatusError as exc:
        # Raise an HTTPException with the same status code and error details
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=exc.response.json() 
        )
    except Exception as exc:
        # Handle non-HTTP exceptions
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred while fetching the profile.: {exc}"
        )
