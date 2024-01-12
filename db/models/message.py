#!/usr/bin/env python3

"""This is a message model module.
"""

from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


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
    date: Mapped[str] = mapped_column(
        String(100),
        default=datetime.now(),
        nullable=False
    )
    sent_from: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    def to_dict(self):
        """Return the object as a dictionary
        """
        return {
            'guest_id': self.guest_id,
            'host_id': self.host_id,
            'content': self.data,
            'datetime': self.date,
            'sent_from': self.sent_from
        }
