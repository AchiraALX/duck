#!/user/bin/env python3

"""The duck messenger module
"""

import asyncio
from quart import render_template, websocket
from quart_auth import login_required
from . import duck_messenger

import secrets
from typing import Any, Dict


host_clients: Dict[str, Any] = {}
guest_clients: Dict[str, Any] = {}


@duck_messenger.route(
        '/',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
@login_required
async def dashboard():
    """Render the dashboard
    """

    host_token = secrets.token_urlsafe(16)

    return await render_template('dashboard.html', host_token=host_token)


@duck_messenger.route(
        '/chat',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
async def chat():
    """Render the chatting window
    """

    guest_token = secrets.token_urlsafe(16)

    return await render_template('code.html', guest_token=guest_token)


# Create a websocket connection
@duck_messenger.websocket('/ws')  # type: ignore
async def ws():
    """Create a websocket connection
    """

    client_connection = websocket._get_current_object()  # type: ignore
    print(client_connection)

    print(f'Connected host clients: {host_clients}')
    print(f'Connnected guest_clients: {guest_clients}')

    try:
        while True:
            # Receive and process the message
            message = await websocket.receive_json()
            print(f'Received: {message}')

            if message.get('type') == 'connect':
                client = message.get('client')

                if client == 'host':
                    host_clients[message.get('token')] = client_connection
                    print(f'Connected clients: {host_clients}')

                if client == 'guest':
                    guest_clients[message.get('token')] = client_connection
                    print(f'Connected guest clients: {guest_clients}')

            if message.get('type') == 'message':
                host_token = message.get('host_token')
                guest_token = message.get('guest_token')

                # Send message to both connections
                print(f'Sending to {host_token} and {guest_token}')
                if host_token in host_clients and guest_token in guest_clients:
                    print('Sending message')
                    await send(
                        host_token=host_token,
                        guest_token=guest_token,
                        message=message
                    )

    except asyncio.CancelledError:
        print('Websocket closed')


async def send(host_token, guest_token, message) -> None:
    """Sending the message to both connections
    """

    host_clients[host_token].send_json(message)
    guest_clients[guest_token].send_json(message)