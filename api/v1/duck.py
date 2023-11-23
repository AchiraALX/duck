#!/usr/bin/env python3


"""Welcome to the Duck
"""


from . import duck_app
from quart import jsonify, Response
from typing import Tuple


@duck_app.route('/', methods=['GET'], strict_slashes=False)
async def duck() -> str:
    """Welcome to duck page
    """

    return jsonify({'duck': 'Ok'})


@duck_app.errorhandler(404)
async def duck_not_found(error) -> Tuple[Response, int]:
    """ 404 Page not found error handler
    """

    return jsonify({'404 error': 'Snap! Its on you end, check URL'}), 404


@duck_app.errorhandler(500)
async def duck_seerver_error(error) -> Tuple[Response, int]:
    """500 internal server error handler
    """

    return jsonify()


@duck_app.errorhandler(403)
async def duck_forbidden(error) -> Tuple[Response, int]:
    """403 forbidden error handler
    """

    return jsonify({'403 error': 'Forbidden'}), 403


@duck_app.errorhandler(401)
async def duck_unauthorized(error) -> Tuple[Response, int]:
    """401 unauthorized error handler
    """

    return jsonify({'401 error': 'Unauthorized'}), 401


@duck_app.errorhandler(400)
async def duck_bad_request(error) -> Tuple[Response, int]:
    """400 bad request error handler
    """

    return jsonify({'400 error': 'Bad request'}), 400