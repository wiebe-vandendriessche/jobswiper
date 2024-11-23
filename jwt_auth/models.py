from database import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(
        String(255), unique=True, index=True
    )  # Added length to String + Indexing
    hashed_password = Column(String(255))  # Added length to String
