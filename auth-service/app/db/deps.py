from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.db.database import SessionLocal
from app.db import token_crud
from app.core.config import SECRET_KEY, ALGORITHM


# -------------------
# DATABASE SESSION
# -------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------
# AUTH SECURITY
# -------------------
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    if token_crud.is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")

        return {
            "email": payload.get("sub"),
            "role": payload.get("role"),
            "token": token
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")