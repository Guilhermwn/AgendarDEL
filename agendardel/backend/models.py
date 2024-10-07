from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel
import uuid

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: EmailStr = Field(index=True, nullable=False)

class UserCreate(UserBase):
    password: str
    
    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 4:
            raise ValueError("Password must be at least 4 characters")
        return value
    
    @field_validator("username")
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError("Username should contain only letters and numbers")
        return value

class UserPublic(UserBase):
    id: uuid.UUID

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str

class UserLogin(SQLModel):
    username: str
    password: str