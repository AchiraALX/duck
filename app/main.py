#!/usr/bin/env python3


"""The duck main module
"""

from quart import redirect, render_template, Response, jsonify, url_for
from typing import Literal, Tuple

from . import duck_app


@duck_app.get('/')
async def main_duck() -> str:
    """Return the main home page for duck app
    """

    return await render_template('index.html')


@duck_app.errorhandler(403)
async def duck_forbidden(error) -> Tuple[Response, int]:
    """403 forbidden error handler
    """

    return jsonify({'403 error': 'Forbidden'}), 403


@duck_app.errorhandler(401)
async def duck_unauthorized(error) -> Tuple[Response, int]:
    """401 unauthorized error handler
    """

    return redirect(url_for('duck_auth.login')), 401


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


@duck_app.errorhandler(404)
async def page_not_found(error) -> Tuple[Response, Literal[404]]:
    """404 page not found error handler
    """
    return redirect(url_for('main_duck')), 404
