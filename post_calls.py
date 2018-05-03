from flask import Flask, render_template, request, session, json, redirect, url_for, Response
from app import app, userdb, postdb
from datetime import datetime

@app.route("/post", methods=["POST"])
def post_attempt():
    if "username" not in session:
        return redirect(url_for('dashboard', username=session["username"]))

    form = dict(request.form)

    if "text" in form and "anonymous" in form:
        text = form["text"][0]
        anonymous = form["anonymous"][0]

        if (anonymous == "True" or anonymous == "False") and text != "":
            for c in text:
                if ord(c) > 127:
                    return False

            postdb.insert_one({
                "user_id": session["user_id"],
                "text": text,
                "date_posted": datetime.now(),
                "anonymous": anonymous
            })
            return 200

    return 400

