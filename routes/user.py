from database.connection import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User, UserSchema, ShowUser, Token
from sqlalchemy.orm import Session
from typing import List
from auth.authenticate import authenticate
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from pydantic import EmailStr

user_router = APIRouter(
    tags=["User"],
)


@user_router.post("/signup")
def sign_user_up(request: UserSchema, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.email == request.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email sudah digunakan."
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password setidaknya memiliki 8 karakter."
        )

    hashed_password = HashPassword().create_hash(request.password)
    new_user = User(email=request.email, nama=request.nama,
                    password=hashed_password, umur = request.umur, daerah = request.daerah)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "Pesan": "Akun berhasil dibuat."
    }


@user_router.post("/signin", response_model=Token)
def sign_user_in(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Akun dengan email tersebut tidak ditemukan."
        )

    if not HashPassword().verify_hash(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Gagal, silahkan periksa email/password Anda kembali!")

    access_token = create_access_token(user.email)

    return {"access_token": access_token, "token_type": "bearer"}

# tidak diimplemetasikan
# @user_router.get("/user", response_model=List[ShowUser])
# def get_user_list(db: Session = Depends(get_db), user: str = Depends(authenticate)) -> dict:
#     admin = db.query(User.email).filter_by(email = 'admin@mail.com')
#     if not admin:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

#     return db.query(User).all()

