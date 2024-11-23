from typing import List, Optional
from pydantic import BaseModel


class Salary(BaseModel):
    min: Optional[float] = None  # Minimum salary
    max: Optional[float] = None  # Maximum salary

    def __repr__(self):
        return f"Salary(min={self.min}, max={self.max})"


class Recruiter(BaseModel):
    id: str  # Unique identifier for the recruiter (from the Profile Management Service)
    name: str  # Name of the recruiter or company
    email: Optional[str] = None  # Optional email for recruiter communication

    def __repr__(self):
        return f"Recruiter(id='{self.id}', name='{self.name}', email='{self.email}')"


class Job(BaseModel):
    job_title: str
    company_name: str
    location: str
    job_type: str  # e.g., 'Full-time', 'Part-time', 'Contract', 'Internship'
    description: str
    requirements: List[str]
    responsibilities: List[str]
    salary: Optional[Salary] = None
    remote: bool = False
    industry: Optional[str] = None
    posted_date: Optional[str] = None
    application_deadline: Optional[str] = None

    def update_salary(self, min: Optional[float] = None, max: Optional[float] = None):
        """Update salary range."""
        if self.salary:
            self.salary.min = min if min is not None else self.salary.min
            self.salary.max = max if max is not None else self.salary.max
        else:
            self.salary = Salary(min=min, max=max)

    def update_description(self, description: str):
        """Update the job description."""
        self.description = description

    def update_requirements(self, requirements: List[str]):
        """Update job requirements."""
        self.requirements = requirements

    def update_responsibilities(self, responsibilities: List[str]):
        """Update job responsibilities."""
        self.responsibilities = responsibilities

    def update_job_type(self, job_type: str):
        """Update the job type."""
        self.job_type = job_type

    def update_application_deadline(self, deadline: Optional[str]):
        """Update the application deadline."""
        self.application_deadline = deadline

    def __repr__(self):
        return (
            f"Job(job_title='{self.job_title}', company_name='{self.company_name}', "
            f"location='{self.location}', job_type='{self.job_type}', "
            f"description='{self.description}', requirements={self.requirements}, "
            f"responsibilities={self.responsibilities}, salary={self.salary}, "
            f"remote={self.remote}, industry='{self.industry}', "
            f"posted_date='{self.posted_date}', application_deadline='{self.application_deadline}')"
        )


class JobListing(BaseModel):
    recruiter: Recruiter  # Recruiter details (referenced from Profile Management Service)
    jobs: List[Job]  # List of jobs

    def add_job(self, job: Job):
        """Add a new job to the listing."""
        self.jobs.append(job)

    def remove_job(self, job_title: str):
        """Remove a job by title."""
        self.jobs = [job for job in self.jobs if job.job_title != job_title]

    def update_job(self, job_title: str, updated_job: Job):
        """Update a job by title."""
        for i, job in enumerate(self.jobs):
            if job.job_title == job_title:
                self.jobs[i] = updated_job
                break

    def __repr__(self):
        return (
            f"JobListing(recruiter={self.recruiter}, jobs=[{', '.join(job.job_title for job in self.jobs)}])"
        )
