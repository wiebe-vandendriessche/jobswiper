from typing import Optional


class Recommendation:
    def __init__(
        self,
        user_id: str,
        job_id: str,
        user_likes: Optional[bool] = None,
        recruiter_likes: Optional[bool] = None,
    ) -> None:
        self.user_id = user_id
        self.job_id = job_id
        self.user_likes = user_likes
        self.recruiter_likes = recruiter_likes

    def swipe_on_user(self, likes: bool) -> None:
        self.recruiter_likes = likes

    def swipe_on_job(self, likes: bool) -> None:
        self.user_likes = likes

    def isMatch(self):
        return self.user_likes and self.recruiter_likes

    def isFinishedRecommending(self) -> bool:
        if self.user_likes and self.recruiter_likes:
            return True
        else:
            return False
