from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    password: str = Column(String(length=1024), nullable=False)