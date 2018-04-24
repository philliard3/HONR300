from flask import Flask, render_template, request, session, json, redirect, url_for, Response
import pymongo
import bson
import datetime

# establish database
client = pymongo.MongoClient()

# database of user accounts
userdb = client.accounttesting.users
postdb = client.accounttesting.posts
commentdb = client.accounttesting.comments
tagdb = client.accounttesting.tags

app = Flask(__name__)
app.secret_key = "change this string"


@app.route("/")
@app.route("/home")
@app.route("/index")
def homepage():
    return render_template("homepage.html")


@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_action():

    # create local instance of the form's response
    form = dict(request.form)

    # stop repeat usernames
    if userdb.find_one({"username": form["username"]}):
        return "username already in db"

    # if the data is valid, insert it
    userdb.insert_one({"username": form["username"], "password": form["password"]})

    # redirect to the login page
    return redirect(url_for('login_page'))


@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_action():

    # create local instance of the form's response
    form = dict(request.form)

    # conduct login if credentials are correct
    if userdb.find_one({"username": form["username"], "password": form["password"]}):
        return "login successful"

    # otherwise redirect to the login page
    return redirect(url_for('login_page'))


@app.route("/post", methods=["GET"])
def make_post():
    return "insert template for post creation page"


@app.route("/post", methods=["POST"])
def add_post():
    form = dict(request.form)

    postdb.insert_one({
        "user_id": form["user_id"],
        "text": form["text"],
        "anonymous": form["anonymous"],
        "date_posted": datetime.datetime.now()
    })


@app.route("/posts", methods=["GET"])
def get_posts():

    result = postdb.find().sort({"date_posted":-1})

    if(result):
        return result[:10]

    return "no posts found"


@app.route("/posts/<str:post_id>", methods=["GET"])
def get_post(post_id):

    result = postdb.find_one({"post_id":post_id})

    if(result):
        return result

    return 400


@app.route("/tag", methods=["GET"])
def make_tag():
    return "insert template for making tag"


@app.route("/tag", methods=["POST"])
def add_tag():
    form = dict(request.form)

    tagdb.insert_one({
        "user_id": form["user_id"],
        "post_id": form["post_id"],
        "text": form["text"],
        "date_posted": datetime.datetime.now()
    })


@app.route("/comment", methods=["GET"])
def make_comment():
    return "insert template for comment creation page"


@app.route("/comment", methods=["POST"])
def add_comment():
    form = dict(request.form)

    commentdb.insert_one({
        "user_id": form["user_id"],
        "post_id": form["post_id"],
        "text": form["text"],
        "date_posted": datetime.datetime.now()
    })


@app.route("/comments", methods=["GET"])
def get_comments():
    result = commentdb.find().sort({"date_posted":-1})

    if(result):
        return result[:10]

    return "no comments found"


@app.route("/comments/<str:comment_id>")
def get_comment(comment_id):
    result = commentdb.find_one({"comment_id": comment_id})

    if (result):
        return result

    return 400


if(__name__=="__main__"):
    userdb.remove()
    postdb.remove()
    commentdb.remove()
    tagdb.remove()
    app.run(debug=True)
    '''
    print(userdb.insert_one({"potato": 1}))
    print(userdb.find_one({"potato":1}))
    print(list(userdb.find()))
    userdb.remove()
    print(userdb.find_one({"potato":1}))
    '''
