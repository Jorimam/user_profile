from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
import logging
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.users import UserResponse, UserCreateRequest, UserUpdateRequest
from ..models.users import User
import bcrypt
import pymysql
from datetime import datetime
from ..enums.enums import Gender
from pydantic import EmailStr



logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user_request:UserCreateRequest, db: Session=Depends(get_db)):

    user_exists = db.query(User).filter(User.email == user_request.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    new_user = User(
        # **user_request.dict(exclude={'password','confirm_password'})
        username=user_request.username,
        email=user_request.email,
        gender=user_request.gender,
        password=hashed_password.decode()
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except pymysql.DataError as e:
        raiseError(e)
    except Exception as e:
        raiseError(e)

def raiseError(e):
    logger.error(f"Failed to create record: {e}")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail= {
            "message": f"Failed to create user: {e}",
            "timestamp": f"{datetime.utcnow()}"
        }
    )
@router.get("/", response_model=List[UserResponse])
def get_all_users(db:Session=Depends(get_db)):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        raiseError(f"Failed to retrieve users: {e}")

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id:int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message":f"User with id {user_id} not found",
                "timestamp":f"{datetime.utcnow()}"
            }
        )
    return user

@router.get("/gender/{gender}", response_model=List[UserResponse])
def get_users_by_gender(gender:Gender, db:Session=Depends(get_db)):
    users = db.query(User).filter(User.gender == gender).all()
    return users

@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(username:str, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email:EmailStr, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id:int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == user_id)
    if not user:
        raiseError(f"User with id {user_id} not found!")
    try:
        user.delete(synchronize_session=False)
        db.commit()
        return{
            "message":"User Deleted Successfully!"
        }
    except Exception as e:
        raiseError(f"Failed to delete user: {e}")

@router.patch("/patch/{user_id}", response_model=UserResponse)
def update_user_by_id(user_id:int, update_user=UserUpdateRequest, db:Session=Depends(get_db)):
    user_exists = db.query(User).filter(User.id == user_id).first()
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message":f"User with id {user_id} not found!"
            
            }
        )
    