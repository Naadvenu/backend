#models/contact.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Contact(BaseModel):
    id: str = None
    name: str
    email: str
    subject: str
    phone: str
    message: str
    created_date: datetime = datetime.now()
    is_read: bool = False
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}
