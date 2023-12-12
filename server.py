#!/usr/bin/env python3

"""Duck server config
"""

from api.v1.duck import duck_app
from jose import jwt

if __name__ == "__main__":
    duck_app.run(port=5000)
