import logging
import os
from fastapi import FastAPI
from typing import Annotated, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from application_layer import JobManagementService

from database import (
    JobRepository,
    SessionLocal,
    Base,
    engine,
)
from publisher import ChangedJobPublisher
from rest_interfaces.job_interfaces import IJob, JobUpdateRequest
from domain_model import Job, Salary

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

Base.metadata.create_all(bind=engine)
app = FastAPI()
publisher = ChangedJobPublisher(
    os.getenv("BUS_SERVICE"),
    int(os.getenv("BUS_PORT", 5672)),
    os.getenv("JOBS_BUS"),
)


@app.on_event("startup")
async def start_publisher():
    await publisher.initialize()


# Initialize the service
service: JobManagementService = JobManagementService(
    JobRepository(SessionLocal), publisher
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/jobs")
async def create_job(job_details: IJob):
    """
    Create a new job.
    - job_details: Details of the job to create.
    """
    job = Job(
        title=job_details.title,
        company_name=job_details.company_name,
        location=job_details.location,
        job_type=job_details.job_type,
        description=job_details.description,
        responsibilities=job_details.responsibilities,
        requirements=job_details.requirements,
        salary=Salary(job_details.salary.min, job_details.salary.max),
        posted_by_uuid=job_details.posted_by_uuid,
    )

    try:
        job_id = await service.register_job(job)
        return JSONResponse(
            content={"message": "Job created successfully", "id": job_id},
            status_code=201,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")

@app.get("/jobs/{job_id}/preview")
async def get_job_preview(job_id: str):
    """
    Get job details by ID.
    - job_id: The ID of the job to fetch.
    """
    try:
        job = await service.get_job_preview(job_id)
        return job
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")

@app.get("/jobs/{recruiter_id}/{job_id}")
async def get_job(job_id: str, recruiter_id: str):
    """
    Get job details by ID.
    - job_id: The ID of the job to fetch.
    - recruiter_id: ID of the recruiter to check authorization
    """
    try:

        job = await service.get_job(job_id, recruiter_id)
        return job
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@app.get("/jobs/{recruiter_id}")
async def list_jobs(recruiter_id: str):
    """
    List all available jobs.
    - recruiter_id: ID of the recruiter to check authorization
    """
    jobs = await service.list_jobs(recruiter_id)
    return jobs


@app.put("/jobs/{recruiter_id}/{job_id}")
async def update_job(job_id: str, recruiter_id: str, updates: JobUpdateRequest):
    """
    Update job details.
    - job_id: ID of the job to update.
    - recruiter_id: ID of the recruiter to check authorization
    - updates: The updates to apply to the job.
    """
    try:
        await service.update_job(job_id, recruiter_id, updates)
        return {"message": "Job updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/jobs/{recruiter_id}/{job_id}")
async def delete_job(job_id: str, recruiter_id: str):
    """
    Delete a job by its ID.
    - job_id: ID of the job to delete.
    - recruiter_id: ID of the recruiter to check authorization
    """
    try:
        await service.delete_job(job_id, recruiter_id)
        return {"message": "Job deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@app.post("/jobs/{recruiter_id}/{job_id}")
async def approve_job(job_id: str, recruiter_id):
    """
    Approve a job for publishing it to the matchmaking service
    - job_id: ID of the job to approve
    - recruiter_id: ID of the recruiter to check authorization
    """
    try:
        job = await service.get_job(job_id, recruiter_id)
        await publisher.job_created(job)
        logger.info(f"JOB PUBLISHED: {job.id}")
        return JSONResponse(
            content={"message": "Job published successfully", "id": job_id},
            status_code=200,
        )
    except ValueError as e:
        logger.warning(f"JOB PUBLISHING FAILED: {job_id}")
        raise HTTPException(status_code=404, delail=str(e))
