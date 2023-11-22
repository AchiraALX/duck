#!/usr/bin/env python3

"""Welcome to the authentication module
"""

from quart import Blueprint, render_template


duck_auth = Blueprint('duck_auth', __name__)
