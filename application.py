import os, requests, json

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
# url: postgres://vutosncbofcbml:cfcc86fa371487684711c172daad8b43267bbdd261171345fc757f87b44dd706@ec2-184-73-174-171.compute-1.amazonaws.com:5432/dnm2k543jrfgv
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("login.html")
    # return render_template("login.html", flights=flights)

@app.route("/register")
def register():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("home.html")
