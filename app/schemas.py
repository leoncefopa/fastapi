# Pydantic Models Schemas
import typing
from datetime import datetime
from typing import Optional, Tuple
from pydantic import BaseModel, EmailStr, conint


# User Data Models
class UserDefault(BaseModel):
    email: EmailStr
    password: str
    phone_number: Optional[str] = None


class UserOutput(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Posts Messages Data Models
class PostBaseInput(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBaseInput):
    rating: Optional[float] = None


class PostBaseOutput(PostBaseInput):
    id: int
    owner_id: int
    created_at: datetime
    owner: UserOutput

    class Config:
        orm_mode = True


class A(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class PostVoteOutput(BaseModel):
    posts: PostBaseOutput
    votes: int


# Votes
class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)


# JWT Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
