#!/usr/bin/env python3

"""This is a message model module.
"""

from . import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Message(Base):
    """This is a message model class.
    """

    __tablename__ = "messages"

    guest_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    host_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    data: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    datetime: Mapped[str] = mapped_column(
        String(100),
        default=datetime.now(),
        nullable=False
    )

    def to_dict(self):
        return {
            'guest_id': self.guest_id,
            'host_id': self.host_id,
            'content': self.data,
            'datetime': self.datetime
        }
