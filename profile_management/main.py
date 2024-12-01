from fastapi import FastAPI
from typing import Annotated, Any, Dict, List, Optional, Union, cast
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from application_layer import ProfileManagementService

from database import (
    JobSeekerRepository,
    RecruiterRepository,
    SessionLocal,
    Base,
    engine,
)
from rest_interfaces.profile_interfaces import (
    IJobSeeker,
    IRecruiter,
    ISalary,
    IUserProfile,
    JobSeekerUpdateRequest,
    RecruiterUpdateRequest,
)

from domain_model import JobSeeker, Recruiter, Salary, UserProfile

Base.metadata.create_all(bind=engine)
app = FastAPI()


service: ProfileManagementService = ProfileManagementService(
    JobSeekerRepository(SessionLocal), RecruiterRepository(SessionLocal)
)


def get_db(self):
    db = self.sessionmaker()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/accounts")
async def create_account(details: Union[IJobSeeker, IRecruiter]):
    """
    Create a new job seeker or recruiter account.
    - account_type: The type of account to create ("job_seeker" or "recruiter").
    - details: The details of the job seeker or recruiter.
    """
    if isinstance(details, IJobSeeker):
        job_seeker = cast(IJobSeeker, details)
        job_seeker = JobSeeker(
            job_seeker.username,
            job_seeker.first_name,
            job_seeker.last_name,
            job_seeker.email,
            job_seeker.interests,
            job_seeker.qualifications,
            job_seeker.location,
            job_seeker.education_level,
            job_seeker.years_of_experience,
            job_seeker.availability,
            Salary(job_seeker.salary.min, job_seeker.salary.max),
            job_seeker.date_of_birth,
            job_seeker.phone_number,
        )

        try:
            await service.register_job_seeker(job_seeker)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    elif isinstance(details, IRecruiter):
        recruiter = cast(IRecruiter, details)
        recruiter = Recruiter(
            recruiter.username,
            recruiter.first_name,
            recruiter.last_name,
            recruiter.email,
            recruiter.location,
            recruiter.company_name,
            recruiter.phone_number,
        )
        try:
            await service.register_recruiter(recruiter)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")
    else:
        raise HTTPException(status_code=400, detail="Invalid account type")

    return JSONResponse(
        content={"message": "Item created successfully"},
        status_code=201,
    )


@app.get("/accounts/{username}")
async def get_account(username: str):
    """
    Get the details of a job seeker or recruiter account by username.
    - username: The username of the account to fetch.
    """
    # Retrieve account by username
    try:
        user = await service.get_user(username)
        return user
    except NameError as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@app.put("/job_seeker/{username}")
async def update_job_seeker(
    username: str,
    updates: JobSeekerUpdateRequest,
):
    try:
        await service.update_job_seeker(username, updates)
        return {"message": "JobSeeker profile updated successfully"}
    except NameError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.put("/recruiter/{username}")
async def update_recruiter(
    username: str,
    updates: RecruiterUpdateRequest,
):
    try:
        await service.update_recruiter(username, company_name=updates.company_name)
        return {"message": "Recruiter profile updated successfully"}
    except NameError as e:
        raise HTTPException(status_code=404, detail=str(e))
