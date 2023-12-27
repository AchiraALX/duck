#!/usr/bin/env python3


"""The duck main module
"""

from quart import render_template
from . import duck_app


@duck_app.get('/')
async def main_duck() -> str:
    """Return the main home page for duck app
    """

    return await render_template('index.html')
