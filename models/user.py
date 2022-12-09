from sqlalchemy import Column, Integer, String
from database.connection import Base
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email= Column(String)
    nama = Column(String)
    password = Column(String)
    umur = Column(Integer)
    daerah = Column(String)


    class Config:
        schema_extra = {
            "example": {
                "email" : "email@mail.com",
                "nama": "Stephanie",
                "password": "password",
                "umur" : 20,
                "daerah" : "Bandung",
            }
        }

class UserSchema(BaseModel):
    email: EmailStr
    nama: str
    password: str
    umur : int
    daerah : str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email" : "email@mail.com",
                "nama" : "Stephanie",
                "password": "password",
                "umur" : 20,
                "daerah" : "Bandung",
            }
        }


class ShowUser(BaseModel):
    email: EmailStr
    nama: str
    umur : int
    daerah : str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email" : "email@mail.com",
                "nama": "Stephanie",
                "umur" : 20,
                "daerah" : "Bandung",
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


    