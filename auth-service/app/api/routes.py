from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db import user_crud
from app.utils.password import verify_password
from app.core.security import create_access_token, create_refresh_token
from app.core.deps import get_current_user
from app.db.token_crud import blacklist_token

router = APIRouter()


# REGISTER
@router.post("/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    if user_crud.get_user_by_email(db, email):
        raise HTTPException(400, "Email already registered")

    user = user_crud.create_user(db, username, email, password)
    return {"message": "User created", "id": user.id}


# LOGIN
@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(400, "Invalid credentials")

    access = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    refresh = create_refresh_token({
        "sub": user.email
    })

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


# PROFILE
@router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"user": user}


# LOGOUT
@router.post("/logout")
def logout(user=Depends(get_current_user)):
    blacklist_token(user["token"])
    return {"message": "Logged out"}