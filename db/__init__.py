#!/usr/bin/env python3


"""Storage module
"""
import json

from typing import Optional
from typing import Any
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import FlushError, NoResultFound
from sqlalchemy.exc import IntegrityError
from .models import Base
from .models.user import User
from .models.message import Message


# DBStorage class declaration
class DBStorage:
    """Handles the connection, reading, writing, updating adn deleting on
    the database
    """

    def __init__(self, drop: Optional = True) -> None:
        """Initialize the class
        """

        self.engine = create_engine('sqlite:///duck.db', echo=False)

        if drop:
            Base.metadata.drop_all(bind=self.engine)

        Base.metadata.create_all(bind=self.engine)

        self.__session = sessionmaker(bind=self.engine)

    def _duck(self) -> Session:
        """Return a new session"""

        return self.__session()

    def add_duck(self, data: Any | None = None) -> Any | None:
        """Commits and saves object to database
        """

        from workers.workers import DuckIntegrityError

        if data is None:
            return None

        try:
            session = self._duck()
            session.add(data)
            session.commit()
            session.flush()

            return data

        except FlushError:
            return None

        except IntegrityError:
            raise DuckIntegrityError from IntegrityError

    def query_duckling(
            self, model: str, query: str) -> Any:
        """Return an object object given a models and fields to query

        Arguments:
            - model [Any | None] -> The actual models that defines the data
            - query [Any | None] -> actual query fields to match
        """

        from workers import DuckNoResultFound

        try:
            if model == 'user':
                result = self._duck().scalars(
                    select(User).where(User.username == query)
                ).first()

                if result is None:
                    raise NoResultFound

                return json.dumps(result.to_dict())

            if model == 'message':
                result = self._duck().scalars(
                    select(Message)
                ).all()

                if result is None:
                    raise NoResultFound

                # Conver the result to a list of dictionaries
                return [message.to_dict() for message in result]

        except NoResultFound:
            raise DuckNoResultFound from NoResultFound

        return None

    def query_duck(self, model: Any) -> Any:
        """Query all fields of a certain model
        """

        if model is None:
            return None

        try:
            result = self._duck().scalars(select(model)).all()
            return result

        except NoResultFound:
            return None

    def __repr__(self) -> str:
        return f"{self.engine} you are good to surf"
