from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database.connection import Base
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class Olahraga(Base):
    __tablename__ = "olahraga"

    id = Column(Integer, primary_key=True)
    olahraga = Column(String, default="")

    class Config:
        schema_extra = {
            "example": {
                "id":1,
                "olahraga": "renang",
            }
        }

class OlahragaSchema(BaseModel):
    olahraga : str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "olahraga" : "renang",
            }
        }