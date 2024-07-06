from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str = None
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False
    registered_date: datetime = datetime.now()
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}
