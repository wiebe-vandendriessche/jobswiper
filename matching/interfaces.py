from abc import ABC, abstractmethod
from typing import List, Optional

from domain_model import Recommendation


class IMatchMakingRepository(ABC):

    @abstractmethod
    async def find_list_of_recommended_jobs(self, user_id: int) -> List[int]:
        pass

    @abstractmethod
    async def find_list_of_recommended_users(self, job_id: int) -> List[int]:
        pass

    @abstractmethod
    async def query(self, user_id: int, job_id: int) -> Optional[Recommendation]:
        pass

    @abstractmethod
    async def save(self, rec: Recommendation) -> None:
        pass
