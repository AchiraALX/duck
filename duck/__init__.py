#!/usr/bin/env python3

"""The duck
"""

from quart import Quart
from secrets import token_hex
from auth.auth import duck_auth

duck_app = Quart(__name__)
duck_app.debug = True
duck_app.secret_key = token_hex()

duck_app.register_blueprint(duck_auth)