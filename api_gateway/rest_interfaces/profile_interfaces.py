from typing import List, Optional
from pydantic import BaseModel

# this file includes objects that are sent to the gateway API regarding the Profilemanagement Service and
# this file includes objects that will be sent to the REST API of the ProfileManagement Service


# -------------------------------------sent to Profile Management Service--------------------------------------------
class Salary(BaseModel):
    min: float = 0
    max: float = 300000


class UserProfile(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    location: str
    phone_number: Optional[str] = None


class JobSeeker(UserProfile):
    qualifications: List[str]
    salary: Salary = Salary()
    education_level: str
    years_of_experience: int
    availability: str
    date_of_birth: Optional[str] = None
    interests: List[str]


class Recruiter(UserProfile):
    company_name: str
