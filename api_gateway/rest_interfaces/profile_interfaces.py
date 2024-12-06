from typing import List, Optional
from pydantic import BaseModel

# this file includes objects that are sent to the gateway API regarding the Profilemanagement Service and
# this file includes objects that will be sent to the REST API of the ProfileManagement Service


# -------------------------------------sent to Profile Management Service--------------------------------------------
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
