#routes/blog.py
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from models.blog import Blog
from models.response_model import create_response
from schemas.blog import BlogSchema, BlogUpdateSchema, BlogResponseSchema
from models.user import User
from middlewares.auth import get_current_active_user
from database.connection import db
from bson import ObjectId
import base64

router = APIRouter()

collection = db.blogs
ModelTitle = "Blog"
Model = Blog
UpdateSchema = BlogUpdateSchema
ResponseSchema = BlogResponseSchema

@router.post("/add")
async def add(
    title: str = Form(...), 
    description: str = Form(...), 
    author: str = Form(...), 
    media: UploadFile = File(None)
):
    try:
        if media:
            file_extension = media.filename.split('.')[-1].lower()
            resource_type = "video" if file_extension in ["mp4", "mov", "avi", "wmv"] else "image"
            
            upload_result = uploader.upload(await media.read(), resource_type=resource_type)
            media_url = upload_result.get("secure_url")

        request_data = Model(title=title, description=description, author=author, media=media_url)
        db_response = collection.insert_one(request_data.dict())
        request_data.id = str(db_response.inserted_id)
        return create_response(f"{ModelTitle} added successfully", 200, "success", ResponseSchema(**dict(request_data.dict(), id=request_data.id)))
    
    except Exception as e:
        return create_response(str(e), 500, "failed")


@router.get("/all")
async def get_all():
    try:
        db_response = list(collection.find({"is_active": True}))
        response = [ResponseSchema(**dict(item, id=str(item["_id"]))) for item in db_response]
        return create_response(f"{ModelTitle} retrieved successfully", 200, "success", response)
    except Exception as e:
        return create_response(str(e), 500, "failed")

@router.get("/{id}")
async def get_by_id(id: str):
    try:
        db_response = collection.find_one({"_id": ObjectId(id), "is_active": True})
        if not db_response:
            raise HTTPException(status_code=404, detail=f"{ModelTitle} not found")

        return create_response(f"{ModelTitle} retrieved successfully", 200, "success", ResponseSchema(**dict(db_response, id=str(db_response["_id"]))))
    
    except Exception as e:
        return create_response(str(e), 500, "failed")


@router.put("/{id}")
async def update(
    id: str, 
    title: str = Form(...), 
    description: str = Form(...), 
    author: str = Form(...), 
    media: UploadFile = File(None)):
    try:
        update_data = {
            "title": title,
            "description": description,
            "author": author
        }

        if media:
            file_extension = media.filename.split('.')[-1].lower()
            resource_type = "video" if file_extension in ["mp4", "mov", "avi", "wmv"] else "image"
            
            upload_result = uploader.upload(await media.read(), resource_type=resource_type)
            media_url = upload_result.get("secure_url")
            update_data["media"] = media_url
        
        db_response = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if db_response.matched_count == 0:
            return create_response(str(e), 404, "failed", f"{ModelTitle} not found")

        updated_data = collection.find_one({"_id": ObjectId(id)})
        if updated_data:
            return create_response(f"{ModelTitle} updated successfully", 200, "success", ResponseSchema(**dict(updated_data, id=str(updated_data["_id"]))))
        else:
            return create_response(str(e), 404, "failed", f"{ModelTitle} not found")
    
    except Exception as e:
        return create_response(str(e), 500, "failed")

@router.put("/{id}/status")
async def activeStatus(id: str, is_active: bool):
    try:
        db_response = collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_active": is_active}})
        if db_response.matched_count == 0:
            return create_response(str(e), 404, "failed", f"{ModelTitle} not found")

        updated_data = collection.find_one({"_id": ObjectId(id)})
        return create_response(f"{ModelTitle} status updated", 200, "success", ResponseSchema(**dict(updated_data, id=str(updated_data["_id"]))))
    
    except Exception as e:
        return create_response(str(e), 500, "failed")

@router.delete("/{id}/")
async def permanentDelete(id: str):
    try:
        db_response = collection.delete_one({"_id": ObjectId(id)})
        if db_response.deleted_count == 0:
            return create_response(f"{ModelTitle} with ID {id} not found", 404, "failed")
        return create_response(f"{ModelTitle} with ID {id} deleted successfully", 200, "success")
    except Exception as e:
        return create_response(str(e), 500, "failed")
