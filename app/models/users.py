from .base import Base
from fastapi import FastAPI
from pydantic import BaseModel
from ..enums.enums import Gender
from enum import Enum
from sqlalchemy import Column, Integer, String, func, DateTime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(25), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    gender = (Column(String(1), nullable=True))
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)