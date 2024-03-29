from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int
    registered_at: datetime