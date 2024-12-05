from typing import Optional, List
from unittest.mock import Base
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Importing the domain models and interfaces
from domain_model import Job, Salary
from interfaces import IJobRepository



class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    location = Column(String(255), nullable=False)
    job_type = Column(String(100), nullable=False)
    salary_min = Column(Float, nullable=False, default=0)
    salary_max = Column(Float, nullable=False, default=300000)
    qualifications = Column(JSON, nullable=True, default=[])
    company_name = Column(String(255), nullable=False)
    posted_by = Column(String(50), nullable=False)
    posted_by_uuid = Column(Integer, nullable=False) # UUID of recruiter -> secondary key
    posted_date = Column(Date, nullable=False)
    application_deadline = Column(Date, nullable=True)


class JobRepository:
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    async def find_by_id(self, job_id: int) -> Optional[Job]:
        db = next(self.get_db())
        job = db.query(JobModel).filter(JobModel.id == job_id).first()
        if job:
            return Job(
                id=job.id,
                title=job.title,
                description=job.description,
                location=job.location,
                job_type=job.job_type,
                salary=Salary(job.salary_min, job.salary_max),
                qualifications=job.qualifications,
                company_name=job.company_name,
                posted_by=job.posted_by,
                posted_date=job.posted_date,
                application_deadline=job.application_deadline,
            )
        return None

    async def save(self, job: Job):
        db = next(self.get_db())
        db_job = JobModel(
            title=job.title,
            description=job.description,
            location=job.location,
            job_type=job.job_type,
            salary_min=job.salary.min,
            salary_max=job.salary.max,
            qualifications=job.qualifications,
            company_name=job.company_name,
            posted_by=job.posted_by,
            posted_date=job.posted_date,
            application_deadline=job.application_deadline,
        )
        if job.id:  # For updating an existing job
            db_job.id = job.id
        db.merge(db_job)  # Check if exists and update or create
        db.commit()

    async def find_all(self, filters: Optional[dict] = None) -> List[Job]:
        db = next(self.get_db())
        query = db.query(JobModel)
        if filters:
            for field, value in filters.items():
                query = query.filter(getattr(JobModel, field) == value)
        jobs = query.all()
        return [
            Job(
                id=job.id,
                title=job.title,
                description=job.description,
                location=job.location,
                job_type=job.job_type,
                salary=Salary(job.salary_min, job.salary_max),
                qualifications=job.qualifications,
                company_name=job.company_name,
                posted_by=job.posted_by,
                posted_date=job.posted_date,
                application_deadline=job.application_deadline,
            )
            for job in jobs
        ]

    async def delete_by_id(self, job_id: int):
        db = next(self.get_db())
        db.query(JobModel).filter(JobModel.id == job_id).delete()
        db.commit()

    def get_db(self):
        db = self.sessionmaker()
        try:
            yield db
        finally:
            db.close()
