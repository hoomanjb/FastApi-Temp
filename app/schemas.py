from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True
