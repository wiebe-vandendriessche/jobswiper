from typing import Optional, List
from abc import ABC, abstractmethod

from domain_model import Job


# Database adapter interface for Job
class IJobRepository(ABC):
    @abstractmethod
    async def save(self, job: Job):
        """Save or update a job in the repository."""
        pass

    @abstractmethod
    async def find_by_id(self, job_id: str, recruiter_id: str) -> Optional[Job]:
        """Retrieve a job by its unique identifier."""
        pass

    @abstractmethod
    async def find_all(self, filters: Optional[dict] = None) -> List[Job]:
        """
        Retrieve all jobs matching the given filters.
        Filters could include attributes like `location`, `job_type`, `salary_range`, etc.
        """
        pass

    @abstractmethod
    async def delete_by_id(self, job_id: str, recruiter_id: str):
        """Delete a job from the repository by its unique identifier."""
        pass


# Message publisher adapter for Job changes
class IChangedJobPublisher(ABC):

    @abstractmethod
    async def job_created(self, job: Job):
        """Notify subscribers about a new job creation."""
        pass

    @abstractmethod
    async def job_updated(self, job: Job):
        """Notify subscribers about a job update."""
        pass

    @abstractmethod
    async def job_deleted(self, job_id: str):
        """Notify subscribers about a job deletion."""
        pass
