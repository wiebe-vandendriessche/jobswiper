from abc import ABC, abstractmethod
from typing import List, Optional

from domain_model import Recommendation
from interfaces import IMatchMakingRepository, IMatchPublisher


class MatchMakingService:
    def __init__(
        self,
        matchmaking_repo: IMatchMakingRepository,
        publisher: IMatchPublisher,
    ):
        self.repo = matchmaking_repo
        self.publisher = publisher

    # self.publisher = publisher

    async def swiped_on_job(self, user_id: int, job_id: int, decision: bool):
        recom: Optional[Recommendation] = await self.repo.query(user_id, job_id)
        if recom:  # else do nothing-> no error because you are consuming from bus
            recom.swipe_on_job(decision)
            await self.changed_recommendation(recom)

    async def swiped_on_user(self, user_id: int, job_id: int, decision: bool):
        recom: Optional[Recommendation] = await self.repo.query(user_id, job_id)
        if recom:  # else do nothing-> no error because you are consuming from bus
            recom.swipe_on_user(decision)
            await self.changed_recommendation(recom)

    async def changed_recommendation(self, recom: Recommendation):
        if (
            recom.isFinishedRecommending()
        ):  # we need to delete it because they both swiped
            if recom.isMatch():
                await self.publisher.found_match(recom)
            await self.repo.delete(
                recom
            )  # only do this after its posted on the bus, otherwise it might have deleted it before and then crashed while publishing it on the bus
        else:  # register the swiping in the database
            await self.repo.save(recom)  # the domain model has already been altered
