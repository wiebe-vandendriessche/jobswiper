from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Uuid


class ISalary(BaseModel):
    min: float = 0
    max: float = 300000


class IJob(BaseModel):
    id: str = None
    title: str
    company_name: str
    location: str
    job_type: str  # e.g., "Full-time", "Part-time", "Contract"
    description: str
    responsibilities: str
    requirements: str
    salary: ISalary = ISalary()
    posted_by: str  # Recruiter's username
    posted_by_uuid: str


class JobCreateRequest(BaseModel):
    id: str = None
    title: str
    company_name: str
    location: str
    job_type: str  # e.g., "Full-time", "Part-time", "Contract"
    description: str
    responsibilities: str
    requirements: str
    salary: ISalary = ISalary()
    posted_by: str  # Recruiter's username
    posted_by_uuid: str


class JobUpdateRequest(BaseModel):
    title: str
    company_name: str
    location: str
    job_type: str  # e.g., "Full-time", "Part-time", "Contract"
    description: str
    responsibilities: str
    requirements: str
    salary: ISalary = ISalary()
    posted_by: str  # Recruiter's username
    posted_by_uuid: str
