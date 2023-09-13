from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, validator, constr, conint, Field


class Book(BaseModel):
    _id: ObjectId
    title: str
    author: str
    description: str


class User(BaseModel):
    _id: ObjectId
    name: str = Field(..., min_length=6, max_length=32)
    password: str = Field(..., min_length=8, max_length=32)
    email: EmailStr

    @validator("password")
    def validate_password_length(cls, value):
        if len(value) < 8 or not value.isalnum():
            raise ValueError("The password must be at least 8 characters long and consist of letters and numbers only.")
        return value


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserProfile(BaseModel):
    name: str
    email: EmailStr


class StatusEnum(str, Enum):
    unread = 'unread'
    read = 'read'


class BookEntry(BaseModel):
    _id: ObjectId
    title: str
    author: str
    description: str
    status: StatusEnum
    mark: Optional[conint(ge=0, le=10)]
    timestamp: datetime


class Shelf(BaseModel):
    _id: ObjectId
    books: List[BookEntry]


