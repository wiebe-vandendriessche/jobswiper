from typing import Dict, List, Optional
from domain_model import Salary, JobSeeker, Recruiter
from interfaces import (
    IChangedJobSeekerPublisher,
    IJobSeekerRepository,
    IRecruiterRepository,
)


class ProfileManagementService:
    def __init__(
        self,
        job_seeker_repo: IJobSeekerRepository,
        recruiter_repo: IRecruiterRepository,
        # publisher: IChangedJobSeekerPublisher,
    ):
        self.job_seeker_repo = job_seeker_repo
        self.recruiter_repo = recruiter_repo

    # self.publisher = publisher

    async def register_job_seeker(self, job_seeker: JobSeeker):
        account = await self.job_seeker_repo.find_by_username(job_seeker.username)
        if account:
            raise NameError(f"User with username:{job_seeker.username} already exists")

        await self.job_seeker_repo.save(job_seeker)
        # await self.publisher.createdProfile(job_seeker)
        return job_seeker

    async def update_job_seeker(self, username: str, kwargs: Dict):
        job_seeker = await self.job_seeker_repo.find_by_username(username)
        if job_seeker:
            if "email" in kwargs:
                job_seeker.update_contact_info(email=kwargs["email"])
            if "phone_number" in kwargs:
                job_seeker.update_contact_info(phone_number=kwargs["phone_number"])
            if "location" in kwargs:
                job_seeker.update_location(kwargs["location"])
            if "availability" in kwargs:
                job_seeker.update_availability(kwargs["availability"])
            if "salary" in kwargs:
                job_seeker.update_salary(kwargs["salary"])
            if "interests" in kwargs:
                job_seeker.update_interests(kwargs["interests"])
            if "qualifications" in kwargs:
                job_seeker.update_qualifications(kwargs["qualifications"])
            await self.job_seeker_repo.save(job_seeker)
            # await self.publisher.updatedProfile(job_seeker)
            return
        raise NameError(f"User with username {username} does not exist.")

    async def register_recruiter(self, recruiter: Recruiter):
        account = await self.recruiter_repo.find_by_username(recruiter.username)
        if account:
            raise NameError(f"User with username:{recruiter.username} already exists")

        await self.recruiter_repo.save(recruiter)
        return recruiter

    async def update_recruiter(self, username: str, company_name: Optional[str] = None):
        recruiter = await self.recruiter_repo.find_by_username(username)
        if recruiter:
            if company_name:
                recruiter.change_company(company_name)
            return
        raise NameError(f"Recruiter with username {username} does not exist.")

    async def get_user(self, username: str):
        recruiter = await self.recruiter_repo.find_by_username(username)
        jobseeker = await self.job_seeker_repo.find_by_username(username)
        if recruiter:
            return recruiter
        if jobseeker:
            return jobseeker
        # in case no users are found
        raise NameError(f"User with username {username} does not exist.")
