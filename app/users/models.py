import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.settings.database import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )

    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )

    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )

    password: Mapped[str] = mapped_column(
        String, nullable=False
    )

    phone_number: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True
    )

    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    )
