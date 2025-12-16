from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional


class UserCreateRequest(BaseModel):
    username:str = Field(min_length=3, max_length=30)
    email:EmailStr
    gender:str
    password: str = Field(min_length=6)
    confirm_password: str

    @field_validator('password')
    def validate_password(cls, value:str):
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit.')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not any(char in "!@#$%^&*()-+" for char in value):
            raise ValueError('Password must contain at least one special character.')
        return value
    @field_validator('username')
    def validate_username(cls, value:str):
        if not value.strip():
            raise ValueError('Username cannot be empty')
        return value

    @model_validator(mode='after')
    def validate_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError('Password does not match')
        return self

class UserResponse(BaseModel):
    id: int 
    username: str 
    email: EmailStr 

class UserUpdateRequest(BaseModel):
    username:Optional[str]=None
    email:Optional[EmailStr]=None 
    gender:Optional[str]
    password:Optional[str]=None

