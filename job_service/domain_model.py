from typing import List, Optional
from datetime import date

from sqlalchemy import Uuid



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
    

class Job:
    def __init__(
        self,
        title: str,
        company_name: str,
        location: str,
        job_type: str,  # e.g., 'Full-time', 'Part-time', 'Contract'
        description: str,
        responsibilities: str,
        requirements: str,
        salary: Salary = Salary(),
        posted_by= str,
        posted_by_uuid= str,
        id: Optional[str] = None,
    ):
        self.title = title  # Job title
        self.company_name = company_name  # Company offering the job
        self.location = location  # Location of the job
        self.job_type = job_type  # Type of employment
        self.description = description  # Job description
        self.responsibilities = responsibilities  # List of job responsibilities
        self.requirements = requirements  # List of job requirements
        self.salary = salary  # Default salary range
        self.posted_by= posted_by
        self.posted_by_uuid= posted_by_uuid
        self.date_posted = date.today().isoformat()  # Date job was posted
        self.id = id  # Unique identifier for the job (optional)

    def update_job_details(
        self,
        title: Optional[str] = None,
        location: Optional[str] = None,
        job_type: Optional[str] = None,
        description: Optional[str] = None,
    ):
        """Update the job details."""
        if title:
            self.title = title
        if location:
            self.location = location
        if job_type:
            self.job_type = job_type
        if description:
            self.description = description

    def update_responsibilities(self, responsibilities: str):
        """Update the list of responsibilities."""
        self.responsibilities = responsibilities

    def update_requirements(self, requirements: str):
        """Update the list of requirements."""
        self.requirements = requirements

    def update_salary(self, min: Optional[float] = None, max: Optional[float] = None):
        """
        Update the salary range.
        This assumes validation is handled by the Salary microservice.
        """
        self.salary.update_salary_range(min,max)

    def __repr__(self):
        return (
            f"Job(title='{self.title}', company_name='{self.company_name}', location='{self.location}', "
            f"job_type='{self.job_type}', salary={self.salary}, date_posted='{self.date_posted}', "
        )


