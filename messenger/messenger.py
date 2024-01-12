#!/user/bin/env python3

"""The duck messenger module
"""

import asyncio
from json import loads
import secrets
from typing import Any, Dict
from quart import render_template, websocket
from quart_auth import login_required, current_user

from workers.workers import Query
from workers.exc import DuckNoResultFound
from db.models.message import Message
from db import DBStorage
from . import duck_messenger


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
    messages = query.query_messages(host_token['username'])

    print(messages)
    print(host_token)

    return await render_template(
        'dashboard.html',
        host_token=host_token['username'],
        messages=messages
    )


@duck_messenger.route(
        '/chat/<host_token>',
        methods=['GET', 'POST'], strict_slashes=False)  # type: ignore
async def chat(host_token: str):
    """Render the chatting window
    """

    guest_token = secrets.token_hex(16)

    print(f'Host token: {host_token.strip()}')
    print(f'Guest token: {guest_token}')

    try:
        host = loads(str(query.query_user(host_token.strip())))
        print(f'Host: {host}')

        return await render_template(
            'code.html',
            host_token=host_token,
            guest_token=guest_token
        )

    except DuckNoResultFound:
        print('No result found')
        return await render_template(
            'signup.html')


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
                host_id = message.get('host_id')
                guest_id = message.get('guest_id')

                # Save the message to the database
                _message = Message(
                    id=secrets.token_hex(16),
                    data=message.get('data'),
                    date=message.get('date'),
                    guest_id=message.get('guest_id'),
                    host_id=message.get('host_id'),
                    sent_from=message.get('sent_from')
                )

                storage.add_duck(_message)

                # Send message to both connections
                print(f'Sending to {host_id} and {guest_id}')
                if host_id in host_clients:
                    await host_clients[host_id].send_json(message)

                if guest_id in guest_clients:
                    await guest_clients[guest_id].send_json(message)

    except asyncio.CancelledError:
        print('Websocket closed')


async def send(host_token, guest_token, message) -> None:
    """Sending the message to both connections
    """

    host_clients[host_token].send_json(message)
    guest_clients[guest_token].send_json(message)
