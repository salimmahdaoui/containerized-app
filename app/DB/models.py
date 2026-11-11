from sqlalchemy import BigInteger, Identity, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
