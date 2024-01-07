#!/user/bin/env python3

"""The duck messenger module
"""

import asyncio
from quart import render_template, websocket
from quart_auth import login_required
from . import duck_messenger

import secrets
from typing import Any, Dict
from quart_auth import current_user


connected_clients: Dict[str, Any] = {}


@duck_messenger.route(
        '/',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
@login_required
async def dashboard():
    """Render the dashboard
    """

    host_token = current_user.auth_id

    return await render_template('dashboard.html', host_token=host_token)


@duck_messenger.route(
        '/chat',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
async def chat():
    """Render the chatting window
    """

    guest_token = secrets.token_urlsafe(16)

    return await render_template('div.html', guest_token=guest_token)


# Create a websocket connection
@duck_messenger.websocket('/ws')  # type: ignore
async def ws():
    """Create a websocket connection
    """

    client_connection = websocket._get_current_object()  # type: ignore
    print(client_connection)

    print(f'Connected clients: {connected_clients}')

    try:
        while True:
            # Receive and process the message
            message = await websocket.receive_json()
            print(f'Received: {message}')

            if message.get('type') == 'connect':
                # Check if the client is already connected
                if message.get('token') in connected_clients:
                    continue

                # Add the client to the connected clients
                connected_clients[message.get('token')] = client_connection
                print(f'Connected clients: {connected_clients}')

            if message.get('type') == 'message':
                # Send the message to the recipient
                recipient = message.get('guest_token')
                print(f'Sending to {recipient}')
                if recipient in connected_clients:
                    print('Sending message')
                    await connected_clients[recipient].send_json(message)

    except asyncio.CancelledError:
        print('Websocket closed')
