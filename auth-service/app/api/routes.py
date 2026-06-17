from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import hash_password, verify_password, create_token
from app.core.security import get_current_user

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return {"error": "Invalid credentials"}

    token = create_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
def profile(current_user=Depends(get_current_user)):
    return {
        "email": current_user,
        "message": "Authenticated"
    }