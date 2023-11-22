#!/usr/bin/env python3

"""Welcome to authentication
"""

from . import duck_auth
from quart import render_template


@duck_auth.route('/login', methods=['GET'], strict_slashes=False)
async def login() -> str:
    """Login main page
    """

    return await render_template('auth/login.html')


@duck_auth.route('/sign-up', methods=['GET'], strict_slashes=False)
async def sign_up () -> str:
    """Sign up main page
    """

    return await render_template('auth/sign-up.html')

