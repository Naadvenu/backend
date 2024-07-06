# schemas/contact.py
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime
from enum import Enum


class ContactSchema(BaseModel):
    name: str
    email: str
    subject: str
    phone: str
    message: str
    is_read: bool = False
    is_active: bool = True

class ContactResponseSchema(BaseModel):
    id: str
    name: str
    email: str
    subject: str
    phone: str
    message: str
    created_date: datetime
    is_read: bool = False
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}

