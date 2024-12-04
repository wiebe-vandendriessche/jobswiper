from abc import ABC, abstractmethod
from typing import List

from domain_model import Recommendation
from interfaces import IMatchMakingRepository


class MatchMakingService:
    def __init__(
        self,
        matchmaking_repo: IMatchMakingRepository,
        # publisher: IMatchPublisher,
    ):
        self.repo = matchmaking_repo

    # self.publisher = publisher

    async def get_recommendations_user(self, user_id: int):
        pass
