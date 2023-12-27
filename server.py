#!/usr/bin/env python3

"""Duck server config
"""

from app.main import duck_app
from jose import jwt

if __name__ == "__main__":
    duck_app.run(port=5000)
