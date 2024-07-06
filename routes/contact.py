#routes/contact.py
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from models.contact import Contact
from models.response_model import create_response
from schemas.contact import ContactSchema, ContactResponseSchema
from models.user import User
from middlewares.auth import get_current_active_user
from database.connection import db
from bson import ObjectId
import base64

router = APIRouter()

collection = db.contacts
ModelTitle = "Contact"
Model = Contact
ResponseSchema = ContactResponseSchema

@router.post("/add")
async def add(
    name: str = Form(...), 
    email: str = Form(...), 
    subject: str = Form(...), 
    phone: str = Form(...), 
    message: str = Form(...)
):
    try:
        request_data = Model(name=name, email=email, subject=subject, phone=phone, message=message)
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

@router.put("/{id}/readStatus")
async def readStatus(id: str, is_read: bool):
    try:
        db_response = collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_read": is_read}})
        if db_response.matched_count == 0:
            return create_response(str(e), 404, "failed", f"{ModelTitle} not found")

        updated_data = collection.find_one({"_id": ObjectId(id)})
        return create_response(f"{ModelTitle} status updated", 200, "success", ResponseSchema(**dict(updated_data, id=str(updated_data["_id"]))))
    
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