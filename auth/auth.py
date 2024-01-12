#!/usr/bin/env python3

"""Welcome to authentication
"""

from json import loads
from typing import Any

from quart import (
    Response,
    abort,
    render_template,
    request,
    url_for,
    redirect,
    flash
)
from quart_auth import (
    AuthUser, current_user, login_user, logout_user
)
from workers.workers import Query, AddToDB, DuckIntegrityError
from workers import DuckNoResultFound

from . import duck_auth

query = Query()
add = AddToDB()


@duck_auth.route('/login', methods=['POST', 'GET'], strict_slashes=False)
async def login() -> Any:
    """Login main page
    """

    if request.method == 'POST':
        username = (await request.form).get('login-username')
        password = (await request.form).get('login-password')

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
                    login_user(AuthUser(user['username']))

                    return redirect(url_for('messenger.dashboard'))
                else:
                    await flash("Invalid password", "error")
                    return redirect(url_for('duck_auth.login'))

        except DuckNoResultFound:
            return redirect(url_for('duck_auth.login'))  # type: ignore

        await flash("Invalid username", "error")
        return redirect(url_for('duck_auth.login'))

    return await render_template('login.html')


@duck_auth.route('/sign-up', methods=['POST', 'GET'], strict_slashes=False)
async def sign_up():
    """Sign up main page
    """

    if request.method == 'POST':
        print("Hello there some dude")
        # Collect user info
        username = (await request.form).get('sign-up-username')
        email = (await request.form).get('sign-up-email')
        password = (await request.form).get('sign-up-password')
        confirm_password = (await request.form).get('sign-up-c-password')

        user = {
            'username': username,
            'email': email,
            'password': password
        }

        print(user)

        # Give response according to inf received
        if username is None:
            await flash("Username must be provided", "error")
            return redirect(url_for('duck_auth.sign_up'))

        if email is None:
            await flash("Email must be provided", "error")
            return redirect(url_for('duck_auth.sign_up'))

        if password is None:
            await flash("Password must be provided", "error")
            return redirect(url_for('duck_auth.sign_up'))

        if confirm_password is None:
            await flash("Confirm password must be provided", "error")
            return redirect(url_for('duck_auth.sign_up'))

        if password != confirm_password:
            await flash("Passwords do not match", "error")
            return redirect(url_for('duck_auth.sign_up'))

        print(f'Username: {username}')

        try:
            add_status = add.add_user({
                'username': username,
                'email': email,
                'password': password
            })

            if add_status is None:
                await flash("An error occured whle adding the user")
                return redirect(url_for('duck_auth.sign_up'))

        except DuckIntegrityError:
            await flash("User already exists")
            return redirect(url_for('duck_auth.login'))

        return redirect(url_for('duck_auth.login'))

    return await render_template('signup.html')


@duck_auth.get('/logout')
async def logout():
    """Log out a user
    """

    if current_user.auth_id is not None:
        logout_user()

        return redirect(url_for('main_duck'))

    return redirect(url_for('duck_auth.login'))


@duck_auth.route('/500', methods=['GET'], strict_slashes=False)
async def cause_500() -> Response:
    """Cause a 500 error
    """

    return abort(500)
