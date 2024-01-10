#!/usr/bin/env python3

"""Welcome to the main duck application
"""

from quart import Quart, request, abort, url_for, redirect
from secrets import token_hex
from auth.auth import duck_auth
from quart_cors import cors
from quart_auth import QuartAuth, current_user
from workers.workers import Auth
import logging
from messenger.messenger import duck_messenger


duck_app = Quart(__name__)
duck_app.debug = True
duck_app.secret_key = token_hex()
duck_app.static_folder = 'static'

logging.basicConfig(level=logging.INFO)

QuartAuth(duck_app)

cors(duck_app, allow_origin='*')
auth = Auth()
excluded_uri = [
    '/login',
    '/sign-up',
    '/ping',
    '/logout',
    '/dashboard/chat',
]

duck_app.register_blueprint(duck_auth)
duck_app.register_blueprint(duck_messenger, url_prefix='/dashboard')


@duck_app.before_request
async def authenticate():
    """Authorize a request
    """
    try:
        logging.info('Processing request...')

        if not auth.require_authorization(request.path, excluded_uri):

            if current_user.auth_id is None:
                return redirect(url_for('duck_auth.login'))

    except Exception as e:
        logging.exception(f'An error occurred: {str(e)}')
        abort(500)
