#!/usr/bin/env python3

"""The duck
"""

from quart import Quart, request, abort
from secrets import token_hex
from auth.auth import duck_auth
from quart_cors import cors
from quart_auth import QuartAuth
from jose import jwt, ExpiredSignatureError, JWTError
from workers.workers import Auth
from typing import Dict

duck_app = Quart(__name__)
duck_app.debug = True
duck_app.secret_key = token_hex()

QuartAuth(duck_app)

cors(duck_app, allow_origin='*')
auth = Auth()
excluded_uri = [
    '/login',
    '/sign-up',
    '/ping',
    '/logout'
]

duck_app.register_blueprint(duck_auth)


@duck_app.before_request
async def authenticate():
    """Authorize a request
    """

    if not auth.requre_authorization(request.path, excluded_uri):

        duck_token = None
        if request.headers.get('Duck-Authorization') is not None:
            duck_token = request.headers.get('Duck-Authorization')

        if request.cookies.get('Duck-Authorization') is not None:
            duck_token = request.cookies.get('Duck-Authorization')

        if request.args.get('authorization') is not None:
            duck_token = request.args.get('authorization')

        try:
            if duck_token is None:
                abort(401)

        except ExpiredSignatureError:
            abort(401)

        except JWTError:
            abort(401)
