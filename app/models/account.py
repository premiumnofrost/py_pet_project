from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    balance: Mapped[int] = mapped_column(default=0, nullable=False)

    user: Mapped["User"] = relationship(
        "User",
        back_populates="accounts"
    )