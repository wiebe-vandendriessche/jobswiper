from typing import List, Optional
import uuid
from pydantic import BaseModel


class Salary:

    def __init__(self, min: float = 0, max: float = 300000):
        self.min = min
        self.max = max

    def update_salary_range(
        self,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ):
        """Update the salary range or currency."""
        if min is not None:
            if max is not None and min > max:
                raise ValueError(
                    "minimum salary cannot be greater than maximum salary."
                )
            self.min = min
        if max is not None:
            if min is not None and max < min:
                raise ValueError("maximum salary cannot be less than minimum salary.")
            self.max = max

    def __repr__(self):
        return f"Salary(min={self.min}$, max={self.max}$')"


class UserProfile:
    def __init__(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        location: str,
        phone_number: Optional[str] = None,
        id: Optional[int] = None,
    ):
        self.username = username
        self.first_name = first_name  # First name of the user
        self.last_name = last_name  # Last name of the user
        self.email = email  # Email address of the user
        self.location = location  # Location of the user
        self.phone_number = phone_number  # Phone number of the user (optional)
        self.id = id

    def update_contact_info(
        self, email: Optional[str] = None, phone_number: Optional[str] = None
    ):
        """Update the contact information."""
        if email:
            self.email = email
        if phone_number:
            self.phone_number = phone_number

    def update_location(self, location: str):
        """Update the user's location."""
        self.location = location

    def __repr__(self):
        return f"UserProfile(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', location='{self.location}', phone_number='{self.phone_number}')"


class JobSeeker(UserProfile):
    def __init__(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        interests: List[str],
        qualifications: List[str],
        location: str,
        education_level: str,
        years_of_experience: int,
        availability: str,
        salary: Salary = Salary(),
        date_of_birth: Optional[str] = None,
        phone_number: Optional[str] = None,
        id: Optional[str] = None,
    ):
        # Initialize parent class with common attributes
        super().__init__(
            username, first_name, last_name, email, location, phone_number, id
        )

        self.qualifications = qualifications  # List of qualifications
        self.salary = salary  # Desired salary range as a Salary object
        self.education_level = education_level  # Highest education level completed
        self.years_of_experience = years_of_experience  # Years of experience
        self.availability = availability  # Availability for starting a new position
        self.date_of_birth = date_of_birth  # Date of birth of the job seeker (optional)
        self.interests = interests

    def update_interests(self, interests: List[str]):
        """Add a new interests to the job seeker's profile."""
        self.interests = interests

    def update_qualifications(self, qualifications: List[str]):
        """Add a new qualifications to the job seeker's profile."""
        self.qualifications = qualifications

    def update_availability(self, availability: str):
        """Update availability status."""
        self.availability = availability

    def update_salary(
        self,
        min: Optional[float] = None,
        max: Optional[float] = None,
    ):
        """Update the salary range using the Salary class's method."""
        self.salary.update_salary_range(min, max)

    def __repr__(self):
        return (
            f"JobSeekerAccount(first_name='{self.first_name}', last_name='{self.last_name}', email='{self.email}', "
            f"qualifications={self.qualifications}, location='{self.location}', "
            f"salary={self.salary}, education_level='{self.education_level}', "
            f"years_of_experience={self.years_of_experience}, availability='{self.availability}')"
        )


class Recruiter(UserProfile):
    def __init__(
        self,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        location: str,
        company_name: str,
        phone_number: Optional[str] = None,
        id: Optional[int] = None,
    ):
        # Initialize parent class with common attributes
        super().__init__(
            username, first_name, last_name, email, location, phone_number, id
        )

        self.company_name = company_name  # Name of the company

    def change_company(self, company: str):
        """Update company"""
        self.company_name = company

    def __repr__(self):
        return (
            f"Recruiter(company_name='{self.company_name}', email='{self.email}' "
            f"location='{self.location}', phone_number='{self.phone_number}')"
        )
