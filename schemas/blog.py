# schemas/blog.py
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime

class BlogSchema(BaseModel):
    title: str
    description: str
    author: str
    img: Optional[str] = None
    is_active: bool = True

class BlogUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    img: Optional[str] = None
    is_active: Optional[bool] = None

class BlogResponseSchema(BaseModel):
    id: str
    title: str
    description: str
    author: str
    created_date : datetime
    img: Optional[str] = None
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}

