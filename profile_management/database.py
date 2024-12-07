from contextlib import contextmanager
import uuid
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
from sqlalchemy import Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.orm import Session
from contextlib import contextmanager
import os

from domain_model import JobSeeker, Recruiter, Salary
from interfaces import IJobSeekerRepository, IRecruiterRepository

DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('DATABASE_SERVICE')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class JobSeekerModel(Base):
    __tablename__ = "job_seekers"
    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    username = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=True)
    education_level = Column(String(100), nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    availability = Column(String(50), nullable=False)
    salary_min = Column(Float, nullable=False, default=0)
    salary_max = Column(Float, nullable=False, default=300000)
    interests = Column(JSON, nullable=False, default=[])
    qualifications = Column(JSON, nullable=False, default=[])
    date_of_birth = Column(Date, nullable=True)


class RecruiterModel(Base):
    __tablename__ = "recruiters"

    id = Column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    username = Column(String(50), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=True)
    company_name = Column(String(100), nullable=False)


class JobSeekerRepository(IJobSeekerRepository):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    async def find_by_username(self, username: str) -> Optional[JobSeeker]:
        with self.get_db() as db:
            job_seeker = (
                db.query(JobSeekerModel)
                .filter(JobSeekerModel.username == username)
                .first()
            )
            if job_seeker:
                return JobSeeker(
                    id=job_seeker.id,
                    username=job_seeker.username,
                    first_name=job_seeker.first_name,
                    last_name=job_seeker.last_name,
                    email=job_seeker.email,
                    location=job_seeker.location,
                    phone_number=job_seeker.phone_number,
                    education_level=job_seeker.education_level,
                    years_of_experience=job_seeker.years_of_experience,
                    availability=job_seeker.availability,
                    salary=Salary(job_seeker.salary_min, job_seeker.salary_max),
                    interests=job_seeker.interests,
                    qualifications=job_seeker.qualifications,
                    date_of_birth=str(job_seeker.date_of_birth),
                )
            return None

    async def save(self, job_seeker: JobSeeker):
        with self.get_db() as db:
            db_job_seeker = JobSeekerModel(
                username=job_seeker.username,
                first_name=job_seeker.first_name,
                last_name=job_seeker.last_name,
                email=job_seeker.email,
                location=job_seeker.location,
                phone_number=job_seeker.phone_number,
                education_level=job_seeker.education_level,
                years_of_experience=job_seeker.years_of_experience,
                availability=job_seeker.availability,
                salary_min=job_seeker.salary.min,
                salary_max=job_seeker.salary.max,
                interests=job_seeker.interests,
                qualifications=job_seeker.qualifications,
                date_of_birth=job_seeker.date_of_birth,
            )
            if job_seeker.id:  # this is for when updating
                db_job_seeker.id = job_seeker.id
            db.merge(db_job_seeker)  # Checks if it exists for updates, otherwise create
            db.commit()

    @contextmanager
    def get_db(self):
        db = self.sessionmaker()
        try:
            yield db
        finally:
            db.close()


class RecruiterRepository(IRecruiterRepository):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    async def find_by_username(self, username: str) -> Optional[Recruiter]:
        with self.get_db() as db:
            recruiter = (
                db.query(RecruiterModel)
                .filter(RecruiterModel.username == username)
                .first()
            )
            if recruiter:
                return Recruiter(
                    username=recruiter.username,
                    first_name=recruiter.first_name,
                    last_name=recruiter.last_name,
                    email=recruiter.email,
                    location=recruiter.location,
                    phone_number=recruiter.phone_number,
                    company_name=recruiter.company_name,
                    id=recruiter.id,
                )
            return None

    async def find_by_uuid(self, uuid: str) -> Optional[Recruiter]:
        with self.get_db() as db:
            recruiter = (
                db.query(RecruiterModel).filter(RecruiterModel.id == uuid).first()
            )
            if recruiter:
                return Recruiter(
                    username=recruiter.username,
                    first_name=recruiter.first_name,
                    last_name=recruiter.last_name,
                    email=recruiter.email,
                    location=recruiter.location,
                    phone_number=recruiter.phone_number,
                    company_name=recruiter.company_name,
                    id=recruiter.id,
                )
            return None

    async def save(self, recruiter: Recruiter):
        with self.get_db() as db:
            db_recruiter = RecruiterModel(
                username=recruiter.username,
                first_name=recruiter.first_name,
                last_name=recruiter.last_name,
                email=recruiter.email,
                location=recruiter.location,
                phone_number=recruiter.phone_number,
                company_name=recruiter.company_name,
            )
            if recruiter.id:  # this is for when updating
                db_recruiter.id = recruiter.id
            db.merge(db_recruiter)  # Checks if it exists for updates, otherwise create
            db.commit()

    @contextmanager
    def get_db(self):
        db = self.sessionmaker()
        try:
            yield db
        finally:
            db.close()
