import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    phone_number: str | None = None
    first_name: str | None = None
    last_name: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone_number: str | None
    first_name: str | None
    last_name: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: EmailStr | None = None
