from typing import List, Optional
from datetime import date
from domain_model import Job
from interfaces import IJobRepository
from rest_interfaces.job_interfaces import JobUpdateRequest


class JobManagementService:
    def __init__(self, job_repo: IJobRepository):
        self.job_repo = job_repo

    async def register_job(self, job: Job):
        exists = await self.check_existing(job.id)
        if exists:
            raise ValueError(f"Job with ID {job.id} already exists.")
        
        await self.job_repo.save(job)
        return job

    async def update_job(self, job_id: int, update: JobUpdateRequest):
        job = await self.job_repo.find_by_id(job_id)
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
        if update.application_deadline:
            job.extend_deadline(update.application_deadline)
        
        await self.job_repo.save(job)

    async def get_job(self, job_id: int) -> Job:
        job = await self.job_repo.find_by_id(job_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} does not exist.")
        return job

    async def list_jobs(self) -> List[Job]:
        jobs = await self.job_repo.list_all()
        return jobs

    async def delete_job(self, job_id: int):
        job = await self.job_repo.find_by_id(job_id)
        if not job:
            raise ValueError(f"Job with ID {job_id} does not exist.")
        await self.job_repo.delete(job_id)

    async def check_existing(self, job_id: Optional[int]) -> bool:
        if job_id is None:
            return False
        job = await self.job_repo.find_by_id(job_id)
        return job is not None
