#!/usr/bin/env python3

"""Workers module
"""
import json
import pickle
from typing import Optional, List, Dict
from quart import jsonify, Response
from db.models.user import User
from db import DBStorage
from typing import List, Union
from .exc import DuckNoResultFound
from sqlalchemy.ext.serializer import loads
import json

storage = DBStorage()


# Auth class declaration
class Auth:
    """Performa simple authentication on the requests
    """
    @staticmethod
    def requre_authorization(
            uri: str | None = None,
            excluded_uris: List[str] | None = None) -> bool:
        """Check if a request needs to be authenticated

        Arguments:
            - uri [str] -> uri to check
            - excluded_uris [list] -> list of urs to exclude

        Return:
            - bool [True | False] True if uri is in excluded_uris else False
        """

        if uri is None or excluded_uris is None:
            return True

        if len(excluded_uris) == 0:
            return True

        if uri.endswith('/'):
            return uri[:-1] in excluded_uris
        else:
            return uri in excluded_uris


class Query:
    """Class for querying the database
    """

    @staticmethod
    def query_user(username: str | None = None) -> User | str:
        """Queries a user from a database
        """

        if username is None:
            return "username has to be provided"

        try:
            user = storage.query_duckling('user', username)
            if user is None:
                raise DuckNoResultFound

            return user

        except DuckNoResultFound:
            raise DuckNoResultFound


class AddToDB:
    """Performs the adding of object to database
    """

    def add_user(self, fields: Dict | None = None) -> User | List | None:
        """Adds user to database

        Arguments:
            - fields -> User fields like username, email, password ...

        Return:
            - User if the required fields are present and user added
              to db correctly
            - None, if fields require don't pass check or fails to add user
        """

        chunks = ['username', 'email', 'password']
        if fields is None:
            return chunks

        result = self._check_fields(fields, chunks)
        if type(result) is bool:
            user = User(**fields)
            try:
                if storage.add_duck(user) is not None:
                    return user

            except DuckIntegrityError:
                raise DuckIntegrityError
        return None

    @staticmethod
    def _check_fields(
            data: Dict | None = None, chunks: List | None = None
    ) -> Union[List[str], bool]:
        """Check fields of given data for the specified chunk

        Arguments:
            - data [duct] -> data to be checked
            - chunks [list] -> fields to check against

        Return:
            - bool. True if all fields present, False otherwise
        """

        failed = list()
        for field in chunks:
            if field not in data:
                failed.append(field)

        if len(failed) > 0:
            return failed

        for key, value in data.items():
            if key in chunks:
                if value is None or not value:
                    failed.append(key)

        if len(failed) > 0:
            return failed

        return True


class MakeErrorResponses:
    """ Builds up error responses from given arguments
    """

    def __init__(self, error: Optional = None, data: Optional = None) -> None:
        """ Initialize class

        Return:
            - None {does not return any value}
        """

        self.error = error if error is not None else None
        self.data = data if data is not None else None

    def make_404(self) -> Response:
        """ Makes a 404 error

        Return:
            - Response {containing details on the error}
        """

        res = {
            'status_code': 404,
            'status': 'Page Not Found',
            'duck': ('Snap! That was on you end, maybe there is a typo'
                     ' on your URL'),
            'reaction': 'sad',
        }

        if self.error is not None:
            res['error'] = str(self.error)

        return jsonify(res)

    def make_500(self) -> Response:
        """Makes a 500 error

        Return:
            - Response
            """

        res = {
            'status_code': 500,
            'status': 'Internal server error.',
            'duck': 'Hang on! That was not you. It is us. Maybe try refresh to'
                    ' see if the issue has been resolved. We are constantly '
                    'on it.',
            'reaction': 'polite',
        }

        if self.error is not None:
            res['error'] = str(self.error)

        return jsonify(res)

    def make_200(self) -> Response:
        """Make an OK response

        Return:
            - Response
        """
        res = {
            'status_code': 200,
            'status': 'OK',
            'duck': 'Whoa! You got it.',
            'reaction': 'happy',
        }

        if self.data is not None:
            res['data'] = self.data

        return jsonify(res)

    def make_401(self):
        """Make unauthorized responses
        """

        res = {
            'status_code': 401,
            'status': 'Unauthorized',
            'duck': 'Nah! Let us do some checks. Can you verify yourself',
            'reaction': 'defensive',
            'redirect': 'login'
        }

        if self.error is not None:
            res['error'] = str(self.error)

        return jsonify(res)


class DuckIntegrityError(Exception):
    """Creates an integrity exception
    """
    pass

