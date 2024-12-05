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
from rest_interfaces.job_interfaces import IJob, JobUpdateRequest
from domain_model import Job, Salary

Base.metadata.create_all(bind=engine)
app = FastAPI()

# Initialize the service
service: JobManagementService = JobManagementService(JobRepository(SessionLocal))


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
        application_deadline=job_details.application_deadline,
    )

    try:
        await service.register_job(job)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    return JSONResponse(
        content={"message": "Job created successfully"},
        status_code=201,
    )


@app.get("/jobs/{job_id}")
async def get_job(job_id: int):
    """
    Get job details by ID.
    - job_id: The ID of the job to fetch.
    """
    try:
        job = await service.get_job(job_id)
        return job
    except ValueError as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@app.get("/jobs")
async def list_jobs():
    """
    List all available jobs.
    """
    jobs = await service.list_jobs()
    return jobs


@app.put("/jobs/{job_id}")
async def update_job(job_id: int, updates: JobUpdateRequest):
    """
    Update job details.
    - job_id: ID of the job to update.
    - updates: The updates to apply to the job.
    """
    try:
        await service.update_job(job_id, updates)
        return {"message": "Job updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/jobs/{job_id}")
async def delete_job(job_id: int):
    """
    Delete a job by its ID.
    - job_id: ID of the job to delete.
    """
    try:
        await service.delete_job(job_id)
        return {"message": "Job deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
