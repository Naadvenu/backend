# schemas/gallery.py
from pydantic import BaseModel
from typing import Optional
from bson import ObjectId
from datetime import datetime
from enum import Enum

class GalleryCategoryEnum(str, Enum):
    eventsWorkshop = "Events - Workshop"
    mentorMentees = "Mentor - Mentees"
    mediaCoverage = "Media Coverage"

class GallerySchema(BaseModel):
    title: str
    category: GalleryCategoryEnum
    media: Optional[str] = None
    author: str
    is_active: bool = True

class GalleryUpdateSchema(BaseModel):
    title: Optional[str] = None
    category: Optional[GalleryCategoryEnum] = None
    author: Optional[str] = None
    media: Optional[str] = None
    is_active: Optional[bool] = None

class GalleryResponseSchema(BaseModel):
    id: str
    title: str
    category: GalleryCategoryEnum
    media: Optional[str] = None
    author: str
    created_date : datetime
    is_active: bool = True

    class Config:
        populate_by_name = True
        alias = {"_id": "id"}

