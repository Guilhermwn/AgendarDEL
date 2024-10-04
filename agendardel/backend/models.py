from typing import Optional
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
import uuid

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)


class UserCreate(UserBase):
    password: str


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str


class UserPublic(UserBase):
    id: uuid.UUID