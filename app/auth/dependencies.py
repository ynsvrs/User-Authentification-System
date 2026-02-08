from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.settings.database import get_db
from app.auth import verify_token
import tables.users as user_tables

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_data = verify_token(token)
    user = db.query(user_tables.Users).filter(user_tables.Users.email == token_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def get_current_active_user(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user
