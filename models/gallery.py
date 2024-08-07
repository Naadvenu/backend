#models/gallery.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Gallery(BaseModel):
    id: str = None
    title: str
    category: str
    media: Optional[str] = None
    author: str
    created_date: datetime = datetime.now()
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}
