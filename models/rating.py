from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database.connection import Base
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True)
    email = Column(String, ForeignKey("users.email"))
    bulutangkis = Column(Integer)
    tenis = Column(Integer)
    sepakbola = Column(Integer)
    voli = Column(Integer)
    renang = Column(Integer)
    lari = Column(Integer)
    tenismeja = Column(Integer)
    golf = Column(Integer)
    senam = Column(Integer)
    basket = Column(Integer)

    class Config:
        schema_extra = {
            "example": {
                "bulutangkis":0,
                "tenis":0,
                "sepakbola":0,
                "voli":0,
                "renang":0,
                "lari":0,
                "tenismeja":0,
                "golf" : 0,
                "senam" :0,
                "basket" :0
            }
        }

class RatingSchema(BaseModel):
    bulutangkis : int
    tenis : int
    sepakbola : int
    voli : int
    renang : int
    lari : int
    tenismeja : int
    golf: int
    senam : int
    basket:int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "bulutangkis":0,
                "tenis":0,
                "sepakbola":0,
                "voli":0,
                "renang":0,
                "lari":0,
                "tenismeja":0,
                "golf" : 0,
                "senam" :0,
                "basket" :0
            }
        }



