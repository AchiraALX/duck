#!/usr/bin/env python3


"""Welcome to the Duck
"""


from . import duck_app
from quart import render_template, websocket


@duck_app.route('/', methods=['GET'], strict_slashes=False)
async def my_duck() -> str:
    """Welcome to duck page
    """

    return await render_template('index.html')
