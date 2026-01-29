from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime.datetime
    updated_at: datetime.datetime

model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: Optional[EmailStr] = None
