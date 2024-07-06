from fastapi import APIRouter, HTTPException, Depends, status
from models.user import User
from schemas.user import UserCreateSchema, UserLoginSchema, UserResponseSchema
from models.response_model import create_response
from database.connection import db
from bson import ObjectId
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from middlewares.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

collection = db.users

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register/admin")
async def register_admin(user: UserCreateSchema):
    user_exist = collection.find_one({"email": user.email})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_data = User(username=user.username, email=user.email, password=hashed_password, is_admin=True)
    db_response = collection.insert_one(user_data.dict())
    user_data.id = str(db_response.inserted_id)
    return UserResponseSchema(**user_data.dict())


@router.post("/register")
async def register(user: UserCreateSchema):
    user_exist = collection.find_one({"email": user.email})
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_data = User(username=user.username, email=user.email, password=hashed_password)
    db_response = collection.insert_one(user_data.dict())
    user_data.id = str(db_response.inserted_id)
    return UserResponseSchema(**user_data.dict())


@router.post("/login")
async def login(user: UserLoginSchema):
    user_data = collection.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not verify_password(user.password, user_data["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data["email"], "is_admin": user_data["is_admin"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users")
async def get_users():
    try:
        db_response = list(collection.find({"is_admin": False, "is_active": True}))
        response = [UserResponseSchema(**dict(item, id=str(item["_id"]))) for item in db_response]
        return create_response(f"Users retrieved successfully", 200, "success", response)
    except Exception as e:
        return create_response(str(e), 500, "failed")


@router.get("/admins")
async def get_admins():
    try:
        db_response = list(collection.find({"is_admin": True, "is_active": True}))
        response = [UserResponseSchema(**dict(item, id=str(item["_id"]))) for item in db_response]
        return create_response(f"Admins retrieved successfully", 200, "success", response)
    except Exception as e:
        return create_response(str(e), 500, "failed")


@router.put("/{id}/is_admin")
async def update_is_admin(id: str, is_admin: bool):
    try:
        db_response = collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_admin": is_admin}})
        if db_response.matched_count == 0:
            return create_response(str(e), 404, "failed", f"User not found")

        updated_data = collection.find_one({"_id": ObjectId(id)})
        if updated_data:
            return create_response(f"User updated successfully", 200, "success", UserResponseSchema(**dict(updated_data, id=str(updated_data["_id"]))))
        else:
            return create_response(str(e), 404, "failed", f"User not found")
    
    except Exception as e:
        return create_response(str(e), 500, "failed")
