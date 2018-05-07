from flask import Flask, render_template, request, session, json, redirect, url_for, Response
from app import app, userdb, postdb, commentdb, tagdb
from datetime import datetime


@app.route("/tag", methods=["POST"])
def add_tag():
    form = dict(request.form)

    if "user_id" in form and ("post_id" in form or "comment_id" in form) and not ("post_id" in form and "comment_id" in form) and "text" in form:
        # verify the user and post exist
        if userdb.find_one({"id": form["user_id"][0]}) and postdb.find_one({"id": form["post_db"][0]}):
            # verify there isn't a sql injection
            if not (';' in form["text"][0] or ')' in form["text"][0]):
                for c in form["text"][0]:
                    if ord(c) > 127:
                        return 400
                if "post_id" in form:
                    if postdb.find_one({"id": form["post_id"][0]}):
                        tagdb.insert_one({
                            "user_id": form["user_id"][0],
                            "post_id": form["post_id"][0],
                            "text": form["text"][0],
                            "date_posted": datetime.datetime.now()
                        })
                else:
                    if commentdb.find_one({"id": form["comment_id"][0]}):
                        tagdb.insert_one({
                            "user_id": form["user_id"][0],
                            "comment_id": form["comment_id"][0],
                            "text": form["text"][0],
                            "date_posted": datetime.datetime.now()
                        })
    return 400


@app.route("/tags/<string:parent_id>", methods=["GET"])
def get_tags(parent_id):
    if str(parent_id).isalnum():
        result = tagdb.find({"post_id": parent_id})
        if result:
            return result
        else:
            result = tagdb.find({"comment_id": parent_id})
            if result:
                return result
    return 400
