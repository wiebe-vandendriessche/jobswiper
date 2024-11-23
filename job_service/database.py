from typing import List, Optional
from sqlalchemy import Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, Text, JSON
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.sqltypes import Date
from sqlalchemy.dialects.mysql import LONGTEXT
from database import Base
import os

from job_service.domain_model import Job, Salary
from job_service.interfaces import IJobRepository

DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@mysql:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=False)
    company_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)  # Simple location field as a string
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    is_remote = Column(Boolean, default=False)


# Repository Implementation
class JobRepository(IJobRepository):
    def __init__(self, db: Session):
        self.db = db

    async def find_by_id(self, job_id: int) -> Optional[Job]:
        db_job = self.db.query(JobModel).filter(JobModel.id == job_id).first()
        if db_job:
            return Job(
                id=db_job.id,
                title=db_job.title,
                description=db_job.description,
                company_name=db_job.company_name,
                location=db_job.location,
                salary=Salary(
                    min=db_job.salary_min,
                    max=db_job.salary_max
                ) if db_job.salary_min and db_job.salary_max else None,
                is_remote=db_job.is_remote
            )
        return None

    async def save(self, job: Job):
        db_job = JobModel(
            id=job.id,
            title=job.title,
            description=job.description,
            company_name=job.company_name,
            location=job.location,
            salary_min=job.salary.min if job.salary else None,
            salary_max=job.salary.max if job.salary else None,
            is_remote=job.is_remote
        )
        self.db.add(db_job)
        self.db.commit()

    async def delete(self, job_id: int):
        db_job = self.db.query(JobModel).filter(JobModel.id == job_id).first()
        if db_job:
            self.db.delete(db_job)
            self.db.commit()

    async def find_all(self) -> List[Job]:
        db_jobs = self.db.query(JobModel).all()
        return [
            Job(
                id=db_job.id,
                title=db_job.title,
                description=db_job.description,
                company_name=db_job.company_name,
                location=db_job.location,
                salary=Salary(
                    min=db_job.salary_min,
                    max=db_job.salary_max
                ) if db_job.salary_min and db_job.salary_max else None,
                is_remote=db_job.is_remote
            )
            for db_job in db_jobs
        ]