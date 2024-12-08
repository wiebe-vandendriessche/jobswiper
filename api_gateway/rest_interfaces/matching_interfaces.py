from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class ISwipe(BaseModel):
    user_id: str
    job_id: str
    recruiter_id: Optional[str]
    decision: bool


@dataclass
class Swipe:
    subject: str  # can be "user" or "job"
    user_id: str
    job_id: str
    decision: bool
