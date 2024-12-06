from typing import Dict, List, Optional
from rest_interfaces.profile_interfaces import JobSeekerUpdateRequest
from domain_model import Salary, JobSeeker, Recruiter
from interfaces import (
    IChangedJobSeekerPublisher,
    IJobSeekerRepository,
    IRecruiterRepository,
)


class ProfileManagementService:
    # DEPENDENCY INJECTION OF ALL ADAPTERS (ONION ARCHITECTURE: ONLY INWARD DEPENDENCIES)
    def __init__(
        self,
        job_seeker_repo: IJobSeekerRepository,
        recruiter_repo: IRecruiterRepository,
        publisher: IChangedJobSeekerPublisher,
    ):
        self.job_seeker_repo = job_seeker_repo
        self.recruiter_repo = recruiter_repo
        self.publisher = publisher

    async def register_job_seeker(self, job_seeker: JobSeeker):
        exists = await self.check_existing(job_seeker.username)
        if exists:
            raise NameError(f"Username already has a coupled profile")

        await self.job_seeker_repo.save(job_seeker)
        await self.publisher.createdProfile(job_seeker)
        return job_seeker

    async def update_job_seeker(self, username: str, update: JobSeekerUpdateRequest):
        job_seeker = await self.job_seeker_repo.find_by_username(username)
        if job_seeker:
            if update.email:
                job_seeker.update_contact_info(email=update.email)
            if update.phone_number:
                job_seeker.update_contact_info(phone_number=update.phone_number)
            if update.location:
                job_seeker.update_location(update.location)
            if update.availability:
                job_seeker.update_availability(update.availability)
            if update.salary:
                job_seeker.update_salary(update.salary.min, update.salary.max)
            if update.interests:
                job_seeker.update_interests(update.interests)
            if update.qualifications:
                job_seeker.update_qualifications(update.qualifications)
            await self.job_seeker_repo.save(job_seeker)
            await self.publisher.updatedProfile(job_seeker)
            return
        raise NameError(f"User with username {username} does not exist.")

    async def register_recruiter(self, recruiter: Recruiter):
        exists = await self.check_existing(recruiter.username)
        if exists:
            raise NameError(f"Username already has a coupled profile")

        await self.recruiter_repo.save(recruiter)
        return recruiter

    async def update_recruiter(self, username: str, company_name: Optional[str] = None):
        recruiter = await self.recruiter_repo.find_by_username(username)
        if recruiter:
            if company_name:
                recruiter.change_company(company_name)
            await self.recruiter_repo.save(recruiter)
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

    async def check_existing(self, username: str):
        account_js = await self.job_seeker_repo.find_by_username(username)
        account_r = await self.recruiter_repo.find_by_username(username)
        # If either returns a non-None object, the username exists
        return account_js is not None or account_r is not None
    
    async def check_existing_uuid(self, uuid: str):
        account = await self.recruiter_repo.find_by_uuid(uuid)
        return account is not None
