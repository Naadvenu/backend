#models/blog.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Blog(BaseModel):
    id: str = None
    title: str
    description: str
    author: str
    img: Optional[str] = None
    created_date: datetime = datetime.now()
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}
