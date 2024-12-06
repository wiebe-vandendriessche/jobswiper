from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from domain_model import Recommendation


class IMatchMakingRepository(ABC):

    @abstractmethod
    async def find_list_of_recommended_jobs(self, user_id: str) -> List[str]:
        pass

    @abstractmethod
    async def find_list_of_recommended_users(self, job_id: str) -> List[str]:
        pass

    @abstractmethod
    async def query(self, user_id: str, job_id: str) -> Optional[Recommendation]:
        pass

    @abstractmethod
    async def save(self, rec: Recommendation) -> None:
        pass

    @abstractmethod
    async def delete(self, rec: Recommendation) -> None:
        pass


class IMatchPublisher(ABC):

    @abstractmethod
    async def found_match(self, user_id: Recommendation) -> None:
        pass


@dataclass
class Swipe:
    subject: str  # can be "user" or "job"
    user_id: str
    job_id: str
    decision: bool
