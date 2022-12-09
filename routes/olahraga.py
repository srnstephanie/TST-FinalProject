from fastapi import APIRouter, Depends, HTTPException, status
from models.olahraga import Olahraga, OlahragaSchema
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from auth.authenticate import authenticate
import sys
from database.connection import get_db
from typing import List
from math import sqrt

olahraga_router = APIRouter(
    tags=['Olahraga'],
)
# belum diimplementasikan
# @olahraga_router.post("/add")
# def sign_user_up(request: OlahragaSchema, db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
#     olahraga = db.query(Olahraga.olahraga).filter(Olahraga.olahraga == request.olahraga and Olahraga.email == user).first()

#     if olahraga:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Olahraga sudah ditambahkan"
#         )

#     new_olahraga = Olahraga(email=user, olahraga = request.olahraga, rating = request.rating)
#     db.add(new_olahraga)
#     db.commit()
#     db.refresh(new_olahraga)

#     return {
#         "Pesan": "Olahraga berhasil ditambahkan."
#     }

@olahraga_router.get("/get", response_model=List[OlahragaSchema])
def get_olahraga(db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
    return db.query(Olahraga).all()
    






