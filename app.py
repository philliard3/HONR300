from flask import Flask, render_template, request, session, json, redirect, url_for, Response
import pymongo
import bson
import datetime

# establish database
client = pymongo.MongoClient()

# database of user accounts
userdb = client.accounttesting.users

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

if(__name__=="__main__"):
    userdb.remove()
    app.run(debug=True)
    '''
    print(userdb.insert_one({"potato": 1}))
    print(userdb.find_one({"potato":1}))
    print(list(userdb.find()))
    userdb.remove()
    print(userdb.find_one({"potato":1}))
    '''
