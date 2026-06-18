from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db import user_crud
from app.utils.security import verify_password
from app.utils.jwt import create_access_token

router = APIRouter()


# REGISTER
@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user_crud.create_user(db, username, email, password)
    return {"message": "User created", "user_id": new_user.id}


# LOGIN
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }