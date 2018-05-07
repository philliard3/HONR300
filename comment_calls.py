from flask import Flask, render_template, request, session, json, redirect, url_for, Response
from app import app, userdb, postdb, commentdb
from datetime import datetime


@app.route("/comment", methods=["POST"])
def comment_attempt():
    form = dict(request.form)

    if "user_id" in form and "post_id" in form and "text" in form:
        # verify the user and post exist
        if userdb.find_one({"id": form["user_id"][0]}) and postdb.find_one({"id": form["post_db"][0]}):
            # verify there isn't a sql injection
            if not (';' in form["text"][0] or ')' in form["text"][0]):
                commentdb.insert_one({
                    "user_id": form["user_id"][0],
                    "post_id": form["post_id"][0],
                    "text": form["text"][0],
                    "date_posted": datetime.datetime.now()
                })


@app.route("/comments", methods=["GET"])
def get_comments():
    result = commentdb.find().sort({"date_posted": -1}).limit(10)

    if result:
        return list(result)

    return "no comments found"


@app.route("/comments/<string:comment_id>")
def get_comment(comment_id):
    result = commentdb.find_one({"comment_id": comment_id})

    if result:
        return list(result)[0]

    return 400


