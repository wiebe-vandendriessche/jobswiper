from typing import List, Optional
from datetime import date
from domain_model import Job
from interfaces import IChangedJobPublisher, IJobRepository
from rest_interfaces.job_interfaces import JobUpdateRequest


class JobManagementService:
    def __init__(self, job_repo: IJobRepository, publisher: IChangedJobPublisher):
        self.job_repo = job_repo
        self.publisher = publisher

    async def register_job(self, job: Job):
        exists = await self.check_existing(job.id, job.posted_by_uuid)
        if exists:
            raise ValueError(f"Job with ID {job.id} already exists.")

        job_id = await self.job_repo.save(job)
        return job_id

    async def update_job(
        self, job_id: str, recruiter_id: str, update: JobUpdateRequest
    ):
        job = await self.job_repo.find_by_id(job_id, recruiter_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} does not exist.")

        if update.title:
            job.update_job_details(title=update.title)
        if update.location:
            job.update_job_details(location=update.location)
        if update.job_type:
            job.update_job_details(job_type=update.job_type)
        if update.description:
            job.update_job_details(description=update.description)
        if update.responsibilities:
            job.update_responsibilities(update.responsibilities)
        if update.requirements:
            job.update_requirements(update.requirements)
        if update.salary:
            job.update_salary(update.salary.min, update.salary.max)

        await self.job_repo.save(job)
        await self.publisher.job_updated(job)

    async def get_job(self, job_id: str, recruiter_id: str) -> Job:
        job = await self.job_repo.find_by_id(job_id, recruiter_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} does not exist.")
        return job

    async def list_jobs(self, recruiter_id: str) -> List[Job]:
        jobs = await self.job_repo.find_all({"posted_by_uuid": recruiter_id})
        return jobs

    async def delete_job(self, job_id: str, recruiter_id: str):
        job = await self.job_repo.find_by_id(job_id, recruiter_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} does not exist.")
        await self.job_repo.delete_by_id(job_id)

    async def check_existing(self, job_id: Optional[str], recruiter_id: str) -> bool:
        if job_id is None:
            return False
        job = await self.job_repo.find_by_id(job_id, recruiter_id)
        return job is not None
