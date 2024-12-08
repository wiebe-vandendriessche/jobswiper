from typing import List
from pydantic import BaseModel


class Match(BaseModel):
    jobseeker_id: str
    job_id: str


class IConversationList(BaseModel):
    is_jobseeker: bool | None
    matches: List[Match]
