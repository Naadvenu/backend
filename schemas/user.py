from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserCreateSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('username')
    def username_must_be_at_least_3_chars(cls, v):
        if len(v) < 3:
            raise ValueError('username must be at least 3 characters long')
        elif v == 'string':
            raise ValueError('invalid username')
        return v

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        if not any(char.isupper() for char in v):
            raise ValueError('password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('password must contain at least one digit')
        return v


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_admin: bool
    registered_date: datetime
    is_active: bool

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}
