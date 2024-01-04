#!/usr/bin/env python3

"""Welcome to authentication
"""

from typing import Any

from flask import flash, redirect
from . import duck_auth
from quart import jsonify, Response, abort, make_response, render_template, request, url_for
from workers import MakeErrorResponses
from workers.workers import Query, AddToDB, DuckIntegrityError
from workers import DuckNoResultFound
from quart_auth import (
    login_user,
    AuthUser,
    current_user,
    logout_user,
)
from jose import jwt
from db.models.user import User
from json import loads

query = Query()
add = AddToDB()


@duck_auth.route('/login', methods=['POST', 'GET'], strict_slashes=False)
async def login() -> Any:
    """Login main page
    """

    if request.method == 'POST':
        username = (await request.form).get('login-username') if \
            request.args.get('username') is None else \
            request.args.get('username')

        password = (await request.form).get('login-password') if \
            request.args.get('password') is None else \
            request.args.get('password')

        if username is None:
            print(username)
            return redirect(url_for('duck_auth.login'))

        if password is None:
            print(password)
            return redirect(url_for('duck_auth.login'))

        try:
            user = loads(str(query.query_user(username)))
            if user['username'] == username:
                if user['password'] == password:
                    from app.main import duck_app
                    token = jwt.encode(
                        user, duck_app.secret_key, algorithm='HS256')
                    login_user(
                        AuthUser(token), remember=True
                    )

                    return redirect(url_for('messenger.dashboard'))
                else:
                    return jsonify({
                        'login': "Invalid password"
                    })
        except DuckNoResultFound:
            return redirect(url_for('duck_auth.login'))  # type: ignore

        return jsonify({
            'login': "Invalid password"
        }), 401

    return await render_template('login.html')


@duck_auth.route('/sign-up', methods=['POST', 'GET'], strict_slashes=False)
async def sign_up() -> Response | str:
    """Sign up main page
    """

    if request.method == 'POST':
        # Collect user info
        username = (await request.form).get('username') if \
            request.args.get('username') is None else \
            request.args.get('username')
        email = (await request.form).get('email') if \
            request.args.get('email') is None else \
            request.args.get('email')
        password = (await request.form).get('password') if \
            request.args.get('password') is None else \
            request.args.get('password')
        confirm_password = (await request.form).get('confirm-password') if \
            request.args.get('confirm-password') is None else \
            request.args.get('confirm-password')

        # Give response according to inf received
        if username is None:
            return jsonify({'sign-up': "Username must be provided"})
        if email is None:
            return jsonify({'sign-up': "Email must be provided"})
        if password is None:
            return jsonify({'sign-up': "Password must be provided."})
        if confirm_password is None:
            return jsonify({'sign-up': "You must confirm you password"})
        if password != confirm_password:
            return jsonify({'sign-up': "Password don't match."})

        try:
            add_status = add.add_user({
                'username': username,
                'email': email,
                'password': password
            })

            if add_status is None:
                return jsonify({'sign-up': f"Error occurred while adding"
                                f" {username}"
                                f" to database"})

        except DuckIntegrityError:
            return jsonify({'sign-up': f"{username} already exists"})
        return jsonify({'sign-up': f"Signed up {username}"})

    return await render_template('signup.html')


@duck_auth.get('/logout')
async def logout():
    """Log out a user
    """

    from app.main import duck_app

    if current_user.auth_id is not None:
        user = jwt.decode(
            current_user.auth_id, duck_app.secret_key, algorithms='HS256'
        ).get('username')
        logout_user()

        return MakeErrorResponses(
            data=f'Sad to see you go {user}! Bye.').make_200()

    return abort(400)


@duck_auth.route('/500', methods=['GET'], strict_slashes=False)
async def cause_500() -> Response:
    """Cause a 500 error
    """

    return abort(500)
