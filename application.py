import os, requests, json

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
# url = "postgres://vutosncbofcbml:cfcc86fa371487684711c172daad8b43267bbdd261171345fc757f87b44dd706@ec2-184-73-174-171.compute-1.amazonaws.com:5432/dnm2k543jrfgv"
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session.pop("username")
    return render_template("login.html")

@app.route("/register", methods=["POST"])
def register():
    """Register an account."""
    session["username"] = request.form.get("username")
    password = request.form.get("password")

    # Make sure that username doesn't already exist
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": session['username']}).rowcount > 0:
        return render_template("error.html", message="Username already exists.", url="index")
    else:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": session["username"], "password": password})

    db.commit()

    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    """Login into existing account."""
    session["username"] = request.form.get("username")
    password = request.form.get("password")

    # Make sure that username and password match to user input
    if db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
        {"username": session["username"], "password": password}).rowcount == 0:
        return render_template("error.html", message="Incorrect username and/or password.", url="index")
    else:
        return render_template("home.html")

@app.route("/search", methods=["POST"])
def search():
    search_request = request.form.get("search").upper()

    if db.execute("SELECT * FROM locations WHERE zipcode LIKE :search_request OR city LIKE :search_request", {"search_request": f"%{search_request}%"}).rowcount == 0:
        return render_template("home.html", message="Failed search", failed_search=True)
    else:
        locations = db.execute("SELECT * FROM locations WHERE zipcode LIKE :search_request OR city LIKE :search_request", {"search_request": f"%{search_request}%"}).fetchall()
        return render_template("home.html", failed_search=False, search_success=True, locations=locations)

