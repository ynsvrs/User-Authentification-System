from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import Users
from app.users.schemas import UserCreate, UserUpdate
from app.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
)

async def create_user(
    db: AsyncSession,
    user: UserCreate
):
    result = await db.execute(
        select(Users).where(
            (Users.email == user.email) |
            (Users.username == user.username)
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="User already exists",
        )

    new_user = Users(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        phone_number=user.phone_number,
        first_name=user.first_name,
        last_name=user.last_name,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
):
    result = await db.execute(
        select(Users).where(Users.email == email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(
        password, user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )

    return create_access_token({"sub": user.email})

async def delete_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Users).where(Users.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()
    return {"detail": f"User {user.username} deleted successfully"}

async def get_user(
    db: AsyncSession,
    user_id: int,
):
    result = await db.execute(
        select(Users).where(Users.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user
