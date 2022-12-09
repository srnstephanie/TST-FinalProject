from database.connection import get_db, getpd
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.rating import Rating, RatingSchema
from models.olahraga import Olahraga
from sqlalchemy.orm import Session
from typing import List
from auth.authenticate import authenticate
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from pydantic import EmailStr
from sklearn.neighbors import NearestNeighbors

rating_router = APIRouter(
    tags=["Rating"],
)

@rating_router.put("/add-rating")
def get_rating(request: RatingSchema, db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
    rating = db.query(Rating).filter(Rating.email == user).first()

    if rating:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rating sudah dibuat, silakan diupdate.")
    
    new_rating = Rating(email=user, bulutangkis = request.bulutangkis, tenis = request.tenis, sepakbola = request.sepakbola, voli = request.voli, renang = request.renang, lari = request.lari, tenismeja = request.tenismeja, golf = request.golf, senam = request.senam, basket=request.basket)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return {
        "Pesan": "Rating berhasil ditambahkan."
    }

@rating_router.put("/update")
def update_rating(request:RatingSchema, db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
    update_rating = db.query(Rating).filter(Rating.email == user)

    if not update_rating.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
    
    update_rating.update({"email":user, "bulutangkis" : request.bulutangkis, "tenis" : request.tenis, "sepakbola" : request.sepakbola, "voli" : request.voli, "renang" : request.renang, "lari" : request.lari, "tenismeja" : request.tenismeja, "golf":request.golf, "senam":request.senam,"basket":request.basket})
    
    db.commit()
    return {"rating berhasil diupdate"}

@rating_router.get("/ratinglist", response_model=List[RatingSchema])
def get_rating_list(db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
    rating = db.query(Rating).filter(Rating.email == user).all()
    
    if not rating:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return rating

@rating_router.get("/kesamaan/{namaolahraga}")
def rekomendasi(namaolahraga:str, db:Session = Depends(get_db), user:str = Depends(authenticate))-> dict:
    check = db.query(Olahraga.olahraga).filter(Olahraga.olahraga == namaolahraga).scalar()

    if not check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")

    df = getpd()
    df = df.transpose()
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(df.values)
    distances, indices = knn.kneighbors(df.values, n_neighbors=3)
    
    for namaolahraga in df.index:
        namaolahraga = str(check)
        index_user_likes = df.index.tolist().index(namaolahraga)
        sim_olahraga = indices[index_user_likes].tolist()
        olahraga_distances = distances[index_user_likes].tolist()
        id_olahraga = sim_olahraga.index(index_user_likes)

        sim_olahraga.remove(index_user_likes)
        olahraga_distances.pop(id_olahraga)
        j = 1
        for i in sim_olahraga:
            return 'Olahraga yang memiliki selisih minimal dengan '+str(df.index[index_user_likes])+' adalah '+str(df.index[i])+'(selisih :  %0.2f'% olahraga_distances[j-1] +') dan '+str(df.index[i+1])+'(selisih : %0.2f' %olahraga_distances[j+1-1]+')'
        