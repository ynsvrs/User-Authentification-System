from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.database import get_db
from app.users import services
from app.users.schemas import (
    UserCreate,
    UserResponse,
    Token,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
@router.post(
    "",
    response_model=UserResponse
)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    return await services.create_user(db, user)

@router.post(
    "/login",
    response_model=Token
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    token = await services.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
    }

@router.delete("/{user_id}")
async def remove_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.delete_user(db, user_id)
