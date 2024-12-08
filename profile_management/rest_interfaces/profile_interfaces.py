from typing import List, Optional
import uuid
from pydantic import BaseModel


class ISalary(BaseModel):
    min: float = 0
    max: float = 300000


class IUserProfile(BaseModel):
    id: Optional[str] = None
    username: str
    first_name: str
    last_name: str
    email: str
    location: str
    phone_number: Optional[str] = None


class IJobSeeker(IUserProfile):
    qualifications: List[str]
    salary: ISalary = ISalary()
    education_level: str
    years_of_experience: int
    availability: str
    date_of_birth: Optional[str] = None
    interests: List[str]


class IRecruiter(IUserProfile):
    company_name: str


class JobSeekerUpdateRequest(
    BaseModel
):  # webapi object only --> not included in domain model
    email: Optional[str] = None
    phone_number: Optional[str] = None
    location: Optional[str] = None
    availability: Optional[str] = None
    salary: Optional[ISalary] = None
    interests: Optional[List[str]] = None
    qualifications: Optional[List[str]] = None


class RecruiterUpdateRequest(BaseModel):
    company_name: Optional[str] = None


class JobseekerPreview(BaseModel):
    first_name: str
    last_name: str
    location: str
    qualifications: List[str]
    salary: ISalary = ISalary()
    education_level: str
    years_of_experience: int
    availability: str
    date_of_birth: Optional[str] = None
    interests: List[str]
