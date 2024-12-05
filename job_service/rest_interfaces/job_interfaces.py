from typing import List, Optional
from pydantic import BaseModel


class ISalary(BaseModel):
    min: float = 0
    max: float = 300000


class IJob(BaseModel):
    title: str
    description: str
    location: str
    job_type: str  # e.g., "Full-time", "Part-time", "Contract"
    salary: ISalary = ISalary()
    qualifications: List[str] = []
    company_name: str
    posted_by: str  # Recruiter's username
    posted_by_uuid: int
    posted_date: str  # ISO format date (e.g., "2024-01-01")
    application_deadline: Optional[str] = None


class JobCreateRequest(BaseModel):
    title: str
    description: str
    location: str
    job_type: str  # e.g., "Full-time", "Part-time", "Contract"
    salary: Optional[ISalary] = ISalary()
    qualifications: Optional[List[str]] = []
    company_name: str
    posted_by: str  # Recruiter's username
    posted_by_uuid: int
    posted_date: str  # ISO format date
    application_deadline: Optional[str] = None


class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[ISalary] = None
    qualifications: Optional[List[str]] = None
    company_name: Optional[str] = None
    application_deadline: Optional[str] = None
