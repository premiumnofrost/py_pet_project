from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    age: Mapped[int] = mapped_column(Integer, nullable=False)

    email: Mapped[str] = mapped_column(String(100), nullable=False)

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

