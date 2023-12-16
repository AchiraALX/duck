#!/usr/bin/env python3


"""Welcome to the duck sql models
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from secrets import token_hex


# Base clas declaration
class Base(DeclarativeBase):
    """Defines the base class for duck models
    """

    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
        default=token_hex(32),
        nullable=False
    )
