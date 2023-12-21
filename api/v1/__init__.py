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
import logging

duck_app = Quart(__name__, template_folder="../../templates, static_folder='../../static'")
duck_app.debug = True
duck_app.secret_key = token_hex()

logging.basicConfig(level=logging.INFO)

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
    try:
        logging.info('Processing request...')

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
                                logging.warning('No Duck token provided.')
                                abort(401)
                        except ExpiredSignatureError:
                            logging.warning('Expired Duck token.')
                            abort(401)

                        except JWTError:
                            logging.warning('Invalid Duck token.')
                            abort(401)

    except Exception as e:
        logging.exception(f'An error occurred: {str(e)}')
        abort(500)
