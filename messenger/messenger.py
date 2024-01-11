#!/user/bin/env python3

"""The duck messenger module
"""

import asyncio
from quart import render_template, websocket
from quart_auth import login_required, current_user
from . import duck_messenger
from workers.workers import Query
from db.models.message import Message
from db import DBStorage

import secrets
from typing import Any, Dict
from json import loads


query = Query()
storage = DBStorage()

host_clients: Dict[str, Any] = {}
guest_clients: Dict[str, Any] = {}


@duck_messenger.route(
        '/',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
@login_required
async def dashboard():
    """Render the dashboard
    """

    host_token = loads(query.query_user(f'{current_user.auth_id}'))

    return await render_template('dashboard.html', host_token=host_token['id'])


@duck_messenger.route(
        '/chat/<host_token>',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
async def chat(host_token: str):
    """Render the chatting window
    """

    try:
        host = loads(str(query.query_user(f'{host_token}')))

        if host is None:
            return await render_template('index.html')

        guest_token = secrets.token_urlsafe(16)

        return await render_template(
            'chat.html', host=str(host_token), guest=guest_token)

    except Exception:
        return await render_template('index.html')


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

                # Save the message to the database
                message = Message(
                    host_token=host_token,
                    guest_token=guest_token,
                    message=message.get('message')
                )

                storage.add_duck(message)

                # Send message to both connections
                print(f'Sending to {host_token} and {guest_token}')
                if host_token in host_clients:
                    await host_clients[host_token].send_json(message)

                if guest_token in guest_clients:
                    await guest_clients[guest_token].send_json(message)

    except asyncio.CancelledError:
        print('Websocket closed')


async def send(host_token, guest_token, message) -> None:
    """Sending the message to both connections
    """

    host_clients[host_token].send_json(message)
    guest_clients[guest_token].send_json(message)
