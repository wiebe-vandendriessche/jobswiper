from typing import List, Optional
from pydantic import BaseModel
from datetime import date


# ------------------------------------- Sent to Job Management Service --------------------------------------------


class ISalary(BaseModel):
    min: float = 0
    max: float = 300000


class IJob(BaseModel):
    id: str
    title: str
    company_name: str
    location: str
    job_type: str  # e.g., 'Full-time', 'Part-time', 'Contract'
    description: str
    responsibilities: List[str]
    requirements: List[str]
    salary: ISalary = ISalary()
    posted_by_uuid: Optional[str] = None
    date_posted: Optional[str] = None
    payment: Optional[int] = 1


class JobUpdateRequest(BaseModel):  # Web API object only --> not included in domain model
    title: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    salary: Optional[ISalary] = None

class IJobPreview(BaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    salary: Optional[ISalary] = None

