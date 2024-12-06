import json
import os
from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
import httpx

from caching import cache_all_jobs, cache_job, get_all_jobs_cache, get_job, remove_all_jobs_cache, remove_job_cache
from rest_interfaces.job_interfaces import IJob, JobUpdateRequest
from main import verify_token_get_user

Jobs_router = APIRouter(prefix="/jobs", tags=["jobs"])

JOB_MANAGEMENT_SERVICE_URL = os.getenv("JOB_MANAGEMENT_SERVICE_URL")


@Jobs_router.post("/")
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
    # if not user.get("is_recruiter", False):
    #     raise HTTPException(
    #         status_code=403, detail="Only recruiters can create job postings."
    #     )

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=job_data.model_dump())
            response.raise_for_status()  # Raise an exception for HTTP errors
            remove_all_jobs_cache()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error from job management service: {exc.response.text}",
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500, detail=f"Internal server error: {str(exc)}"
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
    cache = get_all_jobs_cache()
    if cache:
        return json.loads(cache)

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP errors

            jobs = response.json()  # Assumes the service returns a list of jobs
            cache_all_jobs(json.dumps(jobs))  # Cache the jobs data
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
    cache = get_job(job_id)
    if cache:
        return json.loads(cache)

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{job_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()  # Raise an error for HTTP errors
            cache_job(job_id, response.text)  # Cache the job details
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

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{job_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, json=update_data.model_dump())
            response.raise_for_status()  # Raise an error for HTTP errors
            remove_job_cache(job_id)  # Clear the cache for the updated job
            remove_all_jobs_cache()
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

    url = f"{JOB_MANAGEMENT_SERVICE_URL}/jobs/{job_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(url)
            response.raise_for_status()  # Raise an error for HTTP errors
            remove_job_cache(job_id)
            remove_all_jobs_cache()  # Clear the cache for the deleted job
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
