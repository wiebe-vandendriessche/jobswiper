from typing import Optional, List
from abc import ABC, abstractmethod

from domain_model import JobSeeker, Recruiter


# database adapter interfaces
class IJobSeekerRepository(ABC):
    @abstractmethod
    async def save(self, job_seeker: JobSeeker):
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> JobSeeker:
        pass


class IRecruiterRepository(ABC):
    @abstractmethod
    async def save(self, recruiter: Recruiter):
        pass

    @abstractmethod
    async def find_by_username(self, username: str) -> Optional[Recruiter]:
        pass
    
    @abstractmethod
    async def find_by_uuid(self, uuid: str) -> Optional[Recruiter]:
        pass


# message publisher adapter
class IChangedJobSeekerPublisher(ABC):

    @abstractmethod
    async def updatedProfile(self, seeker: JobSeeker):
        pass

    @abstractmethod
    async def createdProfile(self, seeker: JobSeeker):
        pass
