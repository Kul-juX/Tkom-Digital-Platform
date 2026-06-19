from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_EXPIRE, REFRESH_EXPIRE


def create_access_token(data: dict):
    payload = data.copy()
    payload.update({
        "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRE)
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict):
    payload = data.copy()
    payload.update({
        "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE)
    })
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)