#!/usr/bin/env python3


"""The user model
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Date, String
from . import Base


class User(Base):
    """User model
    """

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    password: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
        }



