from contextlib import contextmanager
from typing import List, Optional
from sqlalchemy import Boolean, Date, Index, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float, JSON
import os

from interfaces import IMatchMakingRepository
from domain_model import Recommendation


DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('DATABASE_SERVICE')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class UserJobMapping(Base):
    __tablename__ = "user_job_mapping"

    user_id = Column(Integer, nullable=False, Index=True, primary_key=True)
    job_id = Column(
        Integer, nullable=False, Index=True, primary_key=True
    )  # because they are combined primary key they are index in a combined way, making them easy to uery as a pair
    user_likes = Column(
        Boolean, nullable=True
    )  # True for "yes", False for "no", None for undecided
    recruiter_likes = Column(
        Boolean, nullable=True
    )  # True for "yes", False for "no", None for undecided


class MySQL_MatchMakingRepo(IMatchMakingRepository):
    def __init__(self, sessionmaker: sessionmaker):
        self.sessionmaker = sessionmaker

    async def find_list_of_recommended_jobs(self, user_id: int) -> List[int]:
        # Using `get_db` to get a session, query all jobs where the user is recommended
        with self.get_db() as db:
            jobs = (
                db.query(UserJobMapping.job_id)
                .filter(UserJobMapping.user_id == user_id)
                .all()
            )
            return [job.job_id for job in jobs]

    async def find_list_of_recommended_users(self, job_id: int) -> List[int]:
        # Using `get_db` to get a session, query all users where the job is recommended
        with self.get_db() as db:
            users = (
                db.query(UserJobMapping.user_id)
                .filter(
                    UserJobMapping.job_id == job_id,
                    UserJobMapping.recruiter_likes == True,
                )
                .all()
            )
            return [user.user_id for user in users]

    async def query(self, user_id: int, job_id: int) -> Optional[Recommendation]:
        # Using `get_db` to get a session, query for a specific user-job recommendation
        with self.get_db() as db:
            result = (
                db.query(UserJobMapping)
                .filter_by(user_id=user_id, job_id=job_id)
                .one_or_none()
            )
            if result:
                return Recommendation(
                    user_id=result.user_id,
                    job_id=result.job_id,
                    user_likes=result.user_likes,
                    recruiter_likes=result.recruiter_likes,
                )
            return None

    async def save(self, rec: Recommendation) -> None:
        # Using `get_db` to get a session, save a new recommendation or update an existing one
        with self.get_db() as db:
            new_record = UserJobMapping(
                user_id=rec.user_id,
                job_id=rec.job_id,
                user_likes=rec.user_likes,
                recruiter_likes=rec.recruiter_likes,
            )
            db.add(new_record)
            db.commit()

    async def delete(self, rec: Recommendation) -> None:
        with self.get_db() as db:
            # Query the record to delete based on user_id and job_id
            record = UserJobMapping(
                user_id=rec.user_id,
                job_id=rec.job_id,
                user_likes=rec.user_likes,
                recruiter_likes=rec.recruiter_likes,
            )
            db.delete(record)  # Delete the found record
            db.commit()  # Commit the transaction to persist the change

    @contextmanager
    def get_db(self):
        db = self.sessionmaker()
        try:
            yield db
        finally:
            db.close()
