import json
import os
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
import httpx

from rabbit import PikaPublisher
from caching import cache_all_jobs, cache_job, get_all_jobs_cache, get_job, remove_all_jobs_cache, remove_job_cache
from rest_interfaces.job_interfaces import IJob, JobUpdateRequest
from main import verify_token_get_user

Jobs_router = APIRouter(prefix="/jobs", tags=["jobs"])

JOB_MANAGEMENT_SERVICE_URL = os.getenv("JOB_MANAGEMENT_SERVICE_URL")
PROFILE_MANAGEMENT_SERVICE_URL = os.getenv("PROFILE_MANAGEMENT_SERVICE_URL")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
QUEUE_NAME = "job_update"

# SAGA
# 1. POST to job_service to add new job to database
# 2. check RecruiterCredentials in profile_management
# 3. check AuthorizeCreditcard in payment_service
# 4a. Publish new job to rabbitmq queue with name="job_update"
# 4b. DELETE to job_service to delete job from database

# ============== Check in PMS -> check_existing
async def check_recruiter_credentials(user_id: str):
    url = f"{PROFILE_MANAGEMENT_SERVICE_URL}/recruiter/{user_id}/credentials"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Recruiter credentials verification failed: {response.text}",
            )
        return response.json()

# ================== Dit zou moeten werken (zie nieuwe payment_service)
async def authorize_credit_card(user_id: str, status: int):
    url = f"{PAYMENT_SERVICE_URL}/authorize"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"user_id": user_id, "status": status})
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Credit card authorization failed: {response.text}",
            )
        return response.json()

# ================= Publishen naar job_update rabbitmq
async def publish_to_rabbitmq(job_id: str, user_id: str):
    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{user_id}/{job_id}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Publishing on queue failed: {response.text}",
            )
        return response.json()



@Jobs_router.post("/")  # START SAGA
async def job_create(
    user: Annotated[dict, Depends(verify_token_get_user)],
    job_data: IJob,
):
    """
    Create a new job posting.

    Args:
        user (dict): The authenticated user's data obtained from the token.
        job_data (IJob): The details of the job to create.

    Returns:
        dict: The response from the Job Management Service.
    """
   

    # Step 1: POST to job_service
    job_id = None
    job_data.posted_by_uuid=user["id"]
    try:
        url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=job_data.model_dump())
            response.raise_for_status()  # Raise exception for HTTP errors
            job_id = response.json().get("id")  # Retrieve job ID
            remove_all_jobs_cache(user["id"])

        # Step 2: Check recruiter credentials
        await check_recruiter_credentials(user["id"])

        # Step 3: Authorize credit card (mocked service)
        # Status is hardcoded to 1 for successful authorization -> extra veld in POST naar api toevoegen om 0 of 1 mee te geven
        await authorize_credit_card(user["id"], status=job_data.payment)

        # Step 4a: Publish to RabbitMQ
        await publish_to_rabbitmq(job_id, user["id"])

        return {"status": "success", "job": response.json()}

    except Exception as exc:
        # Step 4b: Rollback - Delete the job
        if job_id:
            await job_delete(job_id, user)
        raise HTTPException(
            status_code=500,
            detail=f"SAGA failed: {str(exc)}",
        )
        
@Jobs_router.get("/", response_model=list[IJob])
async def get_all_jobs(
    user: Annotated[dict, Depends(verify_token_get_user)],
):
    """
    Retrieve all job postings.

    Args:
        user (dict): The authenticated user's data obtained from the token.

    Returns:
        list[IJob]: A list of all job postings.
    """
        # Check if all jobs are cached
    cache = get_all_jobs_cache(user["id"])
    if cache:
        return json.loads(cache)

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{user["id"]}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP errors

            jobs = response.json()  # Assumes the service returns a list of jobs
            cache_all_jobs(user["id"], json.dumps(jobs))  # Cache the jobs data
            return jobs  # Assumes the service returns a list of jobs
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error from job management service: {exc.response.text}",
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while fetching jobs: {exc}",
            )


@Jobs_router.get("/{job_id}", response_model=IJob)
async def job_get(
    job_id: str,
    user: Annotated[dict, Depends(verify_token_get_user)],
):
    """
    Fetch the details of a job posting by job ID.
    """
    # Check if the job is cached
    cache = get_job(job_id, user["id"])
    if cache:
        return json.loads(cache)

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{user["id"]}/{job_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP errors
            cache_job(job_id, user["id"], response.text)  # Cache the job details
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.json(),
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while fetching the job: {exc}",
            )


@Jobs_router.put("/{job_id}")
async def job_update(
    job_id: str,
    update_data: JobUpdateRequest,
    user: Annotated[dict, Depends(verify_token_get_user)],
):
    """
    Update the details of a job posting by job ID.
    """
    # if not user.get("is_recruiter", False):
    #     raise HTTPException(
    #         status_code=403, detail="Only recruiters can update job postings."
    #     )

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{user["id"]}/{job_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=update_data.model_dump())
            response.raise_for_status()  # Raise an error for HTTP errors
            remove_job_cache(job_id, user["id"])  # Clear the cache for the updated job
            remove_all_jobs_cache(user["id"])
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.json(),
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while updating the job: {exc}",
            )


@Jobs_router.delete("/{job_id}")
async def job_delete(
    job_id: str,
    user: Annotated[dict, Depends(verify_token_get_user)],
):
    """
    Delete a job posting by job ID.
    """
    # if not user.get("is_recruiter", False):
    #     raise HTTPException(
    #         status_code=403, detail="Only recruiters can delete job postings."
    #     )

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{user["id"]}/{job_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(url)
            response.raise_for_status()  # Raise an error for HTTP errors
            remove_job_cache(job_id, user["id"])
            remove_all_jobs_cache(user["id"])  # Clear the cache for the deleted job
            return {"message": "Job deleted successfully"}
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=exc.response.json(),
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred while deleting the job: {exc}",
            )