#!/usr/bin/env python3

"""Duck server config
"""

from app.main import duck_app
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio

# Use hypercorn to serve the app

if __name__ == "__main__":
    config = Config()
    config.bind = ["0.0.0.0:5000"]  # replace with your desired host and port
    asyncio.run(serve(duck_app, config))
