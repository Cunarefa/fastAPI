from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from src.database import Base


# class Post(Base):
#     __tablename__ = "posts"
#
#     title = Column(String(100), nullable=False)
#     body = Column(Text(length=500))
#     author = relationship("User", back_populates="posts")
#     author_id = mapped_column(ForeignKey("users.id"))