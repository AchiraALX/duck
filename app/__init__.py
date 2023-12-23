#!/usr/bin/env python3

"""Welcome to the main duck application
"""

from auth.auth import duck_auth
from messenger.messenger import duck_messenger

from quart import Quart, render_template
from secrets import token_hex
from quart_cors import cors
from quart_auth import QuartAuth, current_user
from workers.workers import Auth
from jose import ExpiredSignatureError, JWTError


duck_app = Quart(__name__)
duck_app.debug = True
duck_app.secret_key = token_hex()


QuartAuth(duck_app)
cors(duck_app, allow_origin='*')
auth = Auth()
excluded_uris = [
    '/login',
    '/sign_up',
    '/ping',
    '/logout'
]

duck_app.register_blueprint(duck_auth)
duck_app.register_blueprint(duck_messenger, url_prefix='/dashboard')


@duck_app.before_request
async def authenticate():
    """Authorize a request if given Duck-Auth value is valid
    """

    pass
