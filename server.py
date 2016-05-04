"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/sign-in", methods=["GET"])
def sign_in_form():
    """Show sign-in form that asks for username and password."""

    return render_template("sign_in.html")


@app.route("/sign-in", methods=["POST"])
def check_user_status():
    """Check if user in database."""

    # Username is email, as user_id autoincrements when user is added to database
    email = request.form.get("email")
    password =  request.form.get("password")

    # Check if user exists in database based on email
    # If not, add user to database
    if db.session.query(User).filter(User.email == email).first():
        return redirect("homepage.html")
    else:
        db.session.add(User(email= email, password = password))
        db.session.commit()
        return redirect("homepage.html")

# NEED TO DO FLASH MESSAGES FOR LOGIN SUCCESS/NOT
@app.route("/log-in", methods=["GET"])
def log_in_form():
    """Show log-in form that asks for username and password."""

    return render_template("login_form.html")


@app.route("/log-in", methods=["POST"])
def check_user_password_match():
    """Check if user password matches against user email."""

    # Username is email, as user_id autoincrements when user is added to database
    email = request.form.get("email")
    password =  request.form.get("password")

    # we want to check user password against user email 
    # if matches then user login redirects to homepage
    # else user gets flash message that says incorrect password

    # if user email and password matches we redirct them to the homepage
    # if not we redirect them back to the login page
    if db.session.query(User).filter(User.email == email, User.password == password).first():
        session["logged_in_user_email"] = email
        flash("Login SUCCESS.")
        return redirect("/")
    else:
        flash("Incorrect password. Please try again!")
        return redirect("/log-in")


@app.route("/log-out")
def process_logout():
    """Log user out."""

    del session["logged_in_user_email"]
    flash("Logged out.")
    return redirect("/")

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
