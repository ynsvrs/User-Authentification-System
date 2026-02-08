from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.settings.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)
MAX_BCRYPT_LENGTH = 72

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
    return pwd_context.hash(password_bytes)

def verify_password( plain_password: str, hashed_password: str) -> bool:
    plain_bytes = plain_password.encode('utf-8')[:MAX_BCRYPT_LENGTH]
    return pwd_context.verify(plain_bytes, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email = payload.get("sub")
        if not email:
            raise JWTError
        return email
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
