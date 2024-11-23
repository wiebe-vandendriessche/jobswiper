from typing import Optional, List
from abc import ABC, abstractmethod
from job_service.domain_model import Job, JobListing, Recruiter  # Adjust the import paths as necessary


# Database Adapter Interfaces
class IJobRepository(ABC):
    """Interface for job database interactions."""
    
    @abstractmethod
    async def save(self, job: Job):
        """Save a job to the repository."""
        pass

    @abstractmethod
    async def find_by_title(self, title: str) -> Optional[Job]:
        """Find a job by its title."""
        pass

    @abstractmethod
    async def delete_by_title(self, title: str):
        """Delete a job by its title."""
        pass

    @abstractmethod
    async def find_all(self) -> List[Job]:
        """Retrieve all jobs."""
        pass

    @abstractmethod
    async def update(self, title: str, updated_job: Job):
        """Update a job in the repository."""
        pass


class IJobListingRepository(ABC):
    """Interface for job listing database interactions."""
    
    @abstractmethod
    async def save(self, listing: JobListing):
        """Save a job listing."""
        pass

    @abstractmethod
    async def find_by_recruiter_id(self, recruiter_id: str) -> Optional[JobListing]:
        """Find job listings by recruiter ID."""
        pass

    @abstractmethod
    async def delete_by_recruiter_id(self, recruiter_id: str):
        """Delete job listings by recruiter ID."""
        pass

    @abstractmethod
    async def add_job_to_listing(self, recruiter_id: str, job: Job):
        """Add a job to a recruiter's listing."""
        pass

    @abstractmethod
    async def remove_job_from_listing(self, recruiter_id: str, job_title: str):
        """Remove a job from a recruiter's listing."""
        pass


# Message Publisher Adapter
class IJobEventPublisher(ABC):
    """Interface for publishing job-related events."""
    
    @abstractmethod
    async def job_created(self, job: Job):
        """Publish an event when a job is created."""
        pass

    @abstractmethod
    async def job_updated(self, job: Job):
        """Publish an event when a job is updated."""
        pass

    @abstractmethod
    async def job_deleted(self, job_title: str):
        """Publish an event when a job is deleted."""
        pass


# Recruiter and JobSeeker Interactions
class IRecruiterServiceAdapter(ABC):
    """Interface for interacting with the Recruiter in the Profile Management microservice."""
    
    @abstractmethod
    async def get_recruiter(self, recruiter_id: str) -> Optional[Recruiter]:
        """Fetch recruiter details by ID."""
        pass

    @abstractmethod
    async def validate_recruiter(self, recruiter_id: str) -> bool:
        """Validate if a recruiter exists."""
        pass


class ISalaryServiceAdapter(ABC):
    """Interface for interacting with the  microservice."""
    
    @abstractmethod
    async def validate_salary(self, min_salary: float, max_salary: float) -> bool:
        """Validate the salary range using the Salary microservice."""
        pass
