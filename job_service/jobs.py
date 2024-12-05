from typing import Annotated, cast
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import database
from application_layer import JobService
from database import JobRepository
from domain_model import Job, UserProfile, Salary
from pydantic import BaseModel

router = APIRouter(prefix="/jobs", tags=["jobs"])

# Dependency to get database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Initialize the service with job repository
service: JobService = JobService(JobRepository(db_dependency))

# Pydantic models for job requests/responses
class JobCreateRequest(BaseModel):
    title: str
    description: str
    company_name: str
    location: str
    salary_min: float | None = None
    salary_max: float | None = None
    is_remote: bool = False

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    company_name: str
    location: str
    salary: Salary | None
    is_remote: bool

    class Config:
        orm_mode = True


@router.post("/create", response_model=JobResponse)
async def create_job(job_details: JobCreateRequest, db: Session = Depends(get_db)):
    """
    Create a new job posting.
    - job_details: The details of the job to create.
    """
    job = Job(
        title=job_details.title,
        description=job_details.description,
        company_name=job_details.company_name,
        location=job_details.location,
        salary=Salary(
            min=job_details.salary_min, 
            max=job_details.salary_max
        ) if job_details.salary_min and job_details.salary_max else None,
        is_remote=job_details.is_remote
    )
    try:
        await service.create_job(job)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    
    return JSONResponse(
        content={"message": "Job created successfully", "job": job_details.dict()},
        status_code=201
    )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Get a job by its ID.
    - job_id: The ID of the job to fetch.
    """
    job = await service.get_job_by_id(job_id)
    if job:
        return job
    else:
        raise HTTPException(status_code=404, detail="Job not found")


@router.get("/all", response_model=list[JobResponse])
async def get_all_jobs(db: Session = Depends(get_db)):
    """
    Get all available job postings.
    """
    jobs = await service.get_all_jobs()
    return jobs


@router.delete("/{job_id}", status_code=204)
async def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a job posting by its ID.
    - job_id: The ID of the job to delete.
    """
    try:
        await service.delete_job(job_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to delete job: {e}")
    
    return JSONResponse(content={"message": "Job deleted successfully"}, status_code=204)
