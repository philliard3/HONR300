from flask import Flask, render_template, request, session, json, redirect, url_for, Response
from app import app, userdb, postdb
from datetime import datetime


@app.route("/post", methods=["POST"])
def post_attempt():

    form = dict(request.form)

    if "text" in form and "anonymous" in form:
        text = form["text"][0]
        anonymous = form["anonymous"][0]

        if (anonymous == "True" or anonymous == "False") and text != "":
            for c in text:
                if ord(c) > 127:
                    return 400

            postdb.insert_one({
                "user_id": session["user_id"],
                "text": text,
                "date_posted": datetime.now(),
                "anonymous": anonymous
            })
            return 200

    return 400


@app.route("/posts", methods=["GET"])
def get_posts():

    result = postdb.find().sort({"date_posted":-1}).limit(10)

    if result:
        return list(result)

    return "no posts found"


@app.route("/posts/<string:post_id>", methods=["GET"])
def get_post(post_id):

    result = postdb.find_one({"post_id": post_id})

    if result:
        return list(result)[0]

    return 400

