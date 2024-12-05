from typing import List, Optional
from datetime import date



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
        responsibilities: List[str],
        requirements: List[str],
        salary: Salary = Salary(),
        date_posted: Optional[date] = None,
        application_deadline: Optional[date] = None,
        id: Optional[int] = None,
    ):
        self.title = title  # Job title
        self.company_name = company_name  # Company offering the job
        self.location = location  # Location of the job
        self.job_type = job_type  # Type of employment
        self.description = description  # Job description
        self.responsibilities = responsibilities  # List of job responsibilities
        self.requirements = requirements  # List of job requirements
        self.salary = salary  # Default salary range
        self.date_posted = date_posted if date_posted else date.today()  # Date job was posted
        self.application_deadline = application_deadline  # Deadline for applications
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

    def update_responsibilities(self, responsibilities: List[str]):
        """Update the list of responsibilities."""
        self.responsibilities = responsibilities

    def update_requirements(self, requirements: List[str]):
        """Update the list of requirements."""
        self.requirements = requirements

    def update_salary(self, min: Optional[float] = None, max: Optional[float] = None):
        """
        Update the salary range.
        This assumes validation is handled by the Salary microservice.
        """
        if min is not None:
            self.salary["min"] = min
        if max is not None:
            self.salary["max"] = max

    def extend_deadline(self, new_deadline: date):
        """Extend or set the application deadline."""
        if new_deadline < self.date_posted:
            raise ValueError("Application deadline cannot be earlier than the posting date.")
        self.application_deadline = new_deadline

    def __repr__(self):
        return (
            f"Job(title='{self.title}', company_name='{self.company_name}', location='{self.location}', "
            f"job_type='{self.job_type}', salary={self.salary}, date_posted='{self.date_posted}', "
            f"application_deadline='{self.application_deadline}')"
        )


