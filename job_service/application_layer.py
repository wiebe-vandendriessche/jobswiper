from typing import Dict, List, Optional
from job_service.domain_model import Job, JobListing
from job_service.interfaces import (
    IJobRepository,
    IJobListingRepository,
    IJobEventPublisher,
    IRecruiterServiceAdapter,
    ISalaryServiceAdapter,
)


class JobService:
    def __init__(
        self,
        job_repo: IJobRepository,
        job_listing_repo: IJobListingRepository,
        job_event_publisher: IJobEventPublisher,
        recruiter_service_adapter: IRecruiterServiceAdapter,
        salary_service_adapter: ISalaryServiceAdapter,
    ):
        self.job_repo = job_repo
        self.job_listing_repo = job_listing_repo
        self.job_event_publisher = job_event_publisher
        self.recruiter_service_adapter = recruiter_service_adapter
        self.salary_service_adapter = salary_service_adapter

    async def create_job(self, recruiter_id: str, job: Job):
        """Create a new job listing under a recruiter."""
        recruiter = await self.recruiter_service_adapter.get_recruiter(recruiter_id)
        if not recruiter:
            raise NameError(f"Recruiter with ID {recruiter_id} does not exist.")

        # Validate salary range
        if job.salary and not await self.salary_service_adapter.validate_salary(
            job.salary.min, job.salary.max
        ):
            raise ValueError("Invalid salary range provided.")

        # Save the job to the repository
        await self.job_repo.save(job)

        # Add job to recruiter's listing
        listing = await self.job_listing_repo.find_by_recruiter_id(recruiter_id)
        if listing:
            await self.job_listing_repo.add_job_to_listing(recruiter_id, job)
        else:
            new_listing = JobListing(recruiter=recruiter, jobs=[job])
            await self.job_listing_repo.save(new_listing)

        # Publish job creation event
        await self.job_event_publisher.job_created(job)
        return job

    async def update_job(self, title: str, updates: Dict):
        """Update an existing job."""
        job = await self.job_repo.find_by_title(title)
        if not job:
            raise NameError(f"Job with title '{title}' does not exist.")

        # Apply updates
        if "job_title" in updates:
            job.job_title = updates["job_title"]
        if "description" in updates:
            job.update_description(updates["description"])
        if "requirements" in updates:
            job.update_requirements(updates["requirements"])
        if "responsibilities" in updates:
            job.update_responsibilities(updates["responsibilities"])
        if "salary" in updates:
            min_salary = updates["salary"].get("min")
            max_salary = updates["salary"].get("max")
            if not await self.salary_service_adapter.validate_salary(min_salary, max_salary):
                raise ValueError("Invalid salary range provided.")
            job.update_salary(min=min_salary, max=max_salary)
        if "location" in updates:
            job.location = updates["location"]
        if "job_type" in updates:
            job.update_job_type(updates["job_type"])

        # Save changes
        await self.job_repo.update(title, job)

        # Publish job update event
        await self.job_event_publisher.job_updated(job)

    async def delete_job(self, recruiter_id: str, title: str):
        """Delete a job by title."""
        job = await self.job_repo.find_by_title(title)
        if not job:
            raise NameError(f"Job with title '{title}' does not exist.")

        # Delete the job
        await self.job_repo.delete_by_title(title)

        # Remove job from recruiter's listing
        await self.job_listing_repo.remove_job_from_listing(recruiter_id, title)

        # Publish job deletion event
        await self.job_event_publisher.job_deleted(title)

    async def list_jobs(self) -> List[Job]:
        """List all jobs."""
        return await self.job_repo.find_all()

    async def get_jobs_by_recruiter(self, recruiter_id: str) -> List[Job]:
        """Retrieve all jobs for a specific recruiter."""
        listing = await self.job_listing_repo.find_by_recruiter_id(recruiter_id)
        if not listing:
            raise NameError(f"No jobs found for recruiter with ID {recruiter_id}.")
        return listing.jobs
