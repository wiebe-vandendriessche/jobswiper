from typing import Annotated, Any, Dict, List, Optional, cast
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database
from application_layer import ProfileManagementService
from database import JobSeekerRepository, RecruiterRepository
from domain_model import JobSeeker, Recruiter, Salary, UserProfile

router = APIRouter(prefix="/profiles", tags=["profiles"])


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


service: ProfileManagementService = ProfileManagementService(
    JobSeekerRepository(db_dependency), RecruiterRepository(db_dependency)
)


class JobSeekerUpdateRequest(
    BaseModel
):  # webapi object only --> not included in domain model
    email: Optional[str] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[bool] = None
    salary: Optional[Salary] = None
    interests: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None


class RecruiterUpdateRequest(BaseModel):
    company_name: Optional[str] = None


@router.post("/accounts")
async def create_account(account_type: str, details: UserProfile):
    """
    Create a new job seeker or recruiter account.
    - account_type: The type of account to create ("job_seeker" or "recruiter").
    - details: The details of the job seeker or recruiter.
    """
    if account_type == "job_seeker":
        if not isinstance(details, JobSeeker):
            raise HTTPException(
                status_code=400, detail="Invalid details for job seeker account"
            )
        job_seeker = cast(JobSeeker, details)
        try:
            await service.register_job_seeker(job_seeker)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"{e}")

    elif account_type == "recruiter":
        if not isinstance(details, Recruiter):
            raise HTTPException(
                status_code=400, detail="Invalid details for recruiter account"
            )
        recruiter = cast(Recruiter, details)
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


@router.get("/accounts/{username}", response_model=UserProfile)
async def get_account(username: str, db: Session = Depends(get_db)):
    """
    Get the details of a job seeker or recruiter account by username.
    - username: The username of the account to fetch.
    """
    # Retrieve account by username
    try:
        user = await service.get_user(username)
    except NameError as e:
        raise HTTPException(status_code=404, detail=f"{e}")


@router.put("/job_seeker/{username}")
async def update_job_seeker(
    username: str,
    updates: JobSeekerUpdateRequest,
):
    try:
        await service.update_job_seeker(username, updates.model_dump())
        return {"message": "JobSeeker profile updated successfully"}
    except NameError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/recruiter/{username}")
async def update_recruiter(
    username: str,
    updates: RecruiterUpdateRequest,
):
    try:
        await service.update_recruiter(username, company_name=updates.company_name)
        return {"message": "Recruiter profile updated successfully"}
    except NameError as e:
        raise HTTPException(status_code=404, detail=str(e))
