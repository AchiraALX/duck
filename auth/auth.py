#!/usr/bin/env python3

"""Welcome to authentication
"""

from typing import Any

from . import duck_auth
from quart import (
    jsonify,
    Response,
    abort,
    render_template,
    request,
    url_for,
    redirect,
    flash
)
from workers import MakeErrorResponses
from workers.workers import Query, AddToDB, DuckIntegrityError
from workers import DuckNoResultFound
from quart_auth import (
    AuthUser, current_user, login_user, logout_user
)

from jose import jwt
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
        setattr(current_user, 'is_authenticated', False)
        setattr(current_user, 'auth_id', None)

        return MakeErrorResponses(
            data=f'Sad to see you go {user}! Bye.').make_200()

    return abort(400)


@duck_auth.route('/500', methods=['GET'], strict_slashes=False)
async def cause_500() -> Response:
    """Cause a 500 error
    """

    return abort(500)
