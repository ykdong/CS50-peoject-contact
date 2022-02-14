import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show Main Page"""
    user_id = session["user_id"]
    friends = db.execute("SELECT * FROM people WHERE friend_id = ?", user_id)
    return render_template("index.html", friends=friends)



@app.route("/newcontact", methods=["GET", "POST"])
@login_required
def newcontact():
    """Show add contact page"""

    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Collect data submitted by user
        firstName = request.form.get("firstname")
        lastName = request.form.get("lastname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")

        # Store contact information into database
        db.execute(
            "INSERT INTO people(friend_id, first_name, last_name, phone, email, address) VALUES(?, ?, ?, ?, ?, ?)", user_id, firstName, lastName, phone, email, address)

        # Redirect user to home page
        flash("New Contact Added!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("newcontact.html")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Show add contact page"""

    user_id = session["user_id"]

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Collect data submitted by user
        Password = request.form.get("new_password")
        Password_again = request.form.get("new_confirmation")

        # Ensure both password was submitted
        if not Password or not Password_again:
            return apology("must provide password", 403)

        # Ensure both passwords matchs
        if Password != Password_again:
            return apology("passwords don't match", 400)

        # Hash the password
        Hash = generate_password_hash(Password, method='pbkdf2:sha256', salt_length=8)

        # Insert register information into database(finance.db)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", Hash, user_id)

        # Redirect to home page
        flash("New Password Saved!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changepassword.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Access from data
        Username = request.form.get("username")
        Password = request.form.get("password")
        Password_again = request.form.get("password-again")

        # Ensure username and password was submitted
        if not Username or not Password or not Password_again:
            return apology("must provide username and/or password", 400)

        # Ensure both passwords matchs
        if Password != Password_again:
            return apology("passwords don't match", 400)

        # Ensure username is valid
        is_username_taken = db.execute("SELECT * FROM users WHERE username = ?", Username)
        if len(is_username_taken) == 1:
            return apology("Username is not available", 400)

        # Hash the password
        Hash = generate_password_hash(Password, method='pbkdf2:sha256', salt_length=8)

        # Insert register information into database(finance.db)
        db.execute("INSERT INTO users(username, hash) VALUES(?, ?)", Username, Hash)

        # Remember the user logged in, store the information into session
        rows = db.execute("SELECT * FROM users WHERE username = ?", Username)
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Registered!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")