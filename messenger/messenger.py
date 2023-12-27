#!/user/bin/env python3


"""The duck messenger module
"""

from quart import render_template
from quart_auth import login_required
from . import duck_messenger


@duck_messenger.route('/', methods=['GET', 'POST'], strict_slashes=False)
@login_required
async def dashboard() -> str:
    """Render the dashboard
    """

    return await render_template('dashboard.html')
