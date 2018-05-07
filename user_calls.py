from flask import Flask, render_template, request, session, json, redirect, url_for, Response
from app import app, userdb


def validate_username(username):
    if type(username) == str and len(username) > 3:
        for c in username:
            if ord(c)> 127:
                return False
        # sanitize for sql statements
        if not(';' in username or ')' in username or '+' in username or '/' in username or '\\' in username or '%' in username or '@' in username):
            return True
    return False


def validate_password(password):
    for c in password:
        if ord(c) > 127:
            return False
    if type(password) == str and len(password) > 3:
        # sanitize for sql statements
        if not(';' in password or ')' in password):
            if password.upper != password and password.lower != password:
                return True
    return False


@app.route('/login', methods=["POST"])
def login_attempt():

    form = dict(request.form)

    if "username" in form and "password" in form:

        username = form["username"][0]
        password = form["password"][0]

        userlist = list(userdb.find({"username": username}))
        if len(userlist) > 0:
            if validate_username(username) and validate_password(password) and username == userlist[0]["username"] and userlist[0]["password"]==password:
                session["username"] = username
                session["user_id"] = str(userlist[0]["_id"])
                return redirect(url_for('dashboard', username=session["username"]))

    return redirect(url_for('login_page', failed=True))


@app.route('/logout')
@app.route('/logoutattempt')
def logout_attempt():

    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for('homepage'))


@app.route('/register', methods=["POST"])
def register_attempt():

    form = dict(request.form)

    if "username" in form and "password" in form:
        username = form["username"][0]
        password = form["password"][0]
        # validate and make sure it's not in the userdb already
        if validate_username(username) and validate_password(password) and len(list(userdb.find({"username": username}))) == 0:
            userdb.insert_one({"username": username, "password": password})
            return redirect(url_for('login'))

    return redirect(url_for('register_page'))



