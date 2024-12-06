import json
import os
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
import httpx

from caching import cache_profile, get_profile, remove_profile_cache
from rest_interfaces.profile_interfaces import IJobSeeker, IRecruiter, IUserProfile, JobSeekerUpdateRequest, RecruiterUpdateRequest
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

    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/accounts"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data.model_dump())
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Return the response from the external service
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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP errors
            cache_profile(user["username"],response.text)
            return response.json()
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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=update_data.model_dump())
            response.raise_for_status()  # Raise an error for HTTP errors
            #clear the original cache because you updated the person
            remove_profile_cache(username)
            return response.json()
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
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=update_data.model_dump())
            response.raise_for_status()  # Raise an error for HTTP errors
            #remove from cache
            remove_profile_cache(username)
            return response.json()
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
