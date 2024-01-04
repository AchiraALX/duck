#!/usr/bin/env python3

"""This is a message model module.
"""

import datetime
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
    admin_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
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
            'admin_id': self.admin_id,
            'content': self.content,
            'datetime': self.datetime
        }
