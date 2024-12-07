from contextlib import contextmanager
from typing import Optional, List
from unittest.mock import Base
import uuid
from sqlalchemy import UUID, Uuid, create_engine, Column, Integer, String, Float, JSON, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Importing the domain models and interfaces
from domain_model import Job, Salary
from interfaces import IJobRepository

DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('DATABASE_SERVICE')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=False)
    location = Column(String(255), nullable=False)
    job_type = Column(String(100), nullable=False)
    salary_min = Column(Float, nullable=False, default=0)
    salary_max = Column(Float, nullable=False, default=300000)
    company_name = Column(String(255), nullable=False)
    posted_by = Column(String(50), nullable=False)
    posted_by_uuid = Column(String(36), nullable=False)  # UUID of recruiter -> secondary key
    date_posted = Column(Date, nullable=False)
    responsibilities = Column(String(1000), nullable=True)  # Comma-separated list of responsibilities
    requirements = Column(String(1000), nullable=True)  # Comma-separated list of requirements


class JobRepository:
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    async def find_by_id(self, job_id: str) -> Optional[Job]:
        with self.get_db() as db:
            job = db.query(JobModel).filter(JobModel.id == job_id).first()
            if job:
                return Job(
                    title=job.title,
                    company_name=job.company_name,
                    location=job.location,
                    job_type=job.job_type,
                    description=job.description,
                    responsibilities=job.responsibilities,
                    requirements=job.requirements,
                    salary=Salary(job.salary_min, job.salary_max),
                    posted_by=job.posted_by,
                    posted_by_uuid=job.posted_by_uuid,
                )
            return None

    async def save(self, job: Job):
        with self.get_db() as db:
            db_job = JobModel(
                id=job.id,
                title=job.title,
                company_name=job.company_name,
                location=job.location,
                job_type=job.job_type,
                description=job.description,
                responsibilities=job.responsibilities,
                requirements=job.requirements,
                salary_min=job.salary.min,
                salary_max=job.salary.max,
                posted_by=job.posted_by,
                posted_by_uuid=job.posted_by_uuid,
                date_posted=job.date_posted
            )
            if job.id:  # For updating an existing job
                db_job.id = job.id
            db.merge(db_job)  # Check if exists and update or create
            db.commit()

            return db_job.id

    
    @contextmanager
    def get_db(self):
        db = self.sessionmaker()
        try:
            yield db
        finally:
            db.close()

    async def find_all(self, filters: Optional[dict] = None) -> List[Job]:
        with self.get_db() as db:
            query = db.query(JobModel)
            if filters:
                for field, value in filters.items():
                    query = query.filter(getattr(JobModel, field) == value)
            jobs = query.all()
            return [
                Job(
                    id=job.id,
                    title=job.title,
                    company_name=job.company_name,
                    location=job.location,
                    job_type=job.job_type,
                    description=job.description,
                    responsibilities=job.responsibilities,
                    requirements=job.requirements,
                    salary=Salary(job.salary_min, job.salary_max),
                    posted_by=job.posted_by,
                    posted_by_uuid=job.posted_by_uuid,
                )
                for job in jobs
            ]

    async def delete_by_id(self, job_id: str):
        with self.get_db() as db:
            db.query(JobModel).filter(JobModel.id == job_id).delete()
            db.commit()

    @contextmanager
    def get_db(self):
        db = self.sessionmaker()
        try:
            yield db
        finally:
            db.close()
