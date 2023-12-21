#!/usr/bin/env python3
"""Welcome to the Duck
"""


from . import duck_app
from quart import jsonify, Response, abort, request
from typing import Tuple
from workers import MakeErrorResponses
from quart_auth import current_user, login_required, logout_user
from jose import jwt
import logging
from quart import Quart, render_template


@duck_app.route('/', methods=['POST'], strict_slashes=False)
@login_required
async def duck() -> Response:
    """Welcome to duck page
    """
    user = jwt.decode(
        current_user.auth_id, duck_app.secret_key, algorithms='HS256')

    logging.info(f'Successful login: {user["username"]}')

    return jsonify(
        {
            'duck': 'Ok',
            'authenticated': user
        }
    )


@duck_app.route('/', methods=['GET'], strict_slashes=False)
async def index():
    return await render_template('index.html')


@duck_app.get('/ping')
async def pong():
    """Confirms the api is still alive
    """

    logging.info('Ping request received.')

    return MakeErrorResponses(data="Pong").make_200()


@duck_app.get('/unauthorized')
@login_required
async def unauthorized():
    """Check for the 401 error
    """

    logout_user()
    return abort(401)


@duck_app.errorhandler(404)
async def duck_not_found(error) -> Tuple[Response, int]:
    """ 404 Page not found error handler
    """

    logging.warning('404 Not Found error.')

    return MakeErrorResponses(error).make_404(), 200


@duck_app.errorhandler(500)
async def duck_server_error(error) -> Tuple[Response, int]:
    """500 internal server error handler
    """

    return MakeErrorResponses(error).make_500(), 500


@duck_app.errorhandler(403)
async def duck_forbidden(error) -> Tuple[Response, int]:
    """403 forbidden error handler
    """

    return jsonify({'403 error': 'Forbidden'}), 403


@duck_app.errorhandler(401)
async def duck_unauthorized(error) -> Tuple[Response, int]:
    """401 unauthorized error handler
    """

    return MakeErrorResponses({
        'error': 'Unauthorized',
        'message': 'You are not authorized to access this resource.'
    }).make_401(), 401


@duck_app.errorhandler(400)
async def duck_bad_request(error) -> Tuple[Response, int]:
    """400 bad request error handler
    """

    return jsonify({'400 error': 'Bad request'}), 400


@duck_app.errorhandler(405)
async def method_not_allowed(error) -> Tuple[Response, int]:
    """405 Method not allowed error handler
    """

    return jsonify({'405 error': "Method not allowed"}), 405
