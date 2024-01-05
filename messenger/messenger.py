#!/user/bin/env python3

"""The duck messenger module
"""

from quart import render_template, websocket
from quart_auth import login_required
from . import duck_messenger

import secrets


connected_clients = set()

client_tokens = {}

async def sending(token: str, message: str, sender_token: str):
    """Send a message to a specific user
    """
    
    recipient = client_tokens.get(token, None)
    if recipient:
        await recipient.send(message)
    else:
        await client_tokens[sender_token].send('The recipient is not connected')


async def receive(token: str):
    """Receive a message from a specific user
    """

    return await client_tokens[token].receive()

@duck_messenger.route('/', methods=['GET', 'POST'], strict_slashes=False) #type: ignore
@login_required
async def dashboard():
    """Render the dashboard
    """
    return await render_template('dashboard.html')

@duck_messenger.route('/chat', methods=['GET', 'POST'], strict_slashes=False) #type: ignore
async def chat():
    """Render the chatting window
    """

    return await render_template('div.html')

# Create a websocket connection
@duck_messenger.websocket('/ws') #type: ignore
async def ws():
    """Create a websocket connection
    """
    
    client_token = secrets.token_urlsafe(16)

    connected_clients.add(websocket._get_current_object()) # type: ignore
    client_tokens[client_token] = websocket._get_current_object() # type: ignore

    try:
        while True:
            # Receive a JSON object from the client
            data  = await websocket.receive_json()

            # Extract information from the JSON object
            recipient_token = data['recipient_token']
            sender_token = data['sender_token']
            message = data['message']

            # Check if the recipient is connected
            recipient = client_tokens.get(recipient_token, None)
            if recipient:
                # Send the message to the recipient
                await recipient.send(message)
            else:
                # Send the message to the sender
                await client_tokens[sender_token].send('The recipient is not connected')

    finally:
        # Remove the client from the connected clients set
        connected_clients.remove(websocket._get_current_object()) # type: ignore
        client_tokens.pop(client_token, None)

