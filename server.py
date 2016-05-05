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


# This takes to each user's profile from user list
@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """Show user information"""

    # Query by user id to return that record in database about user info
    user = User.query.filter(User.user_id == user_id).one()

    # Passed user info into jinja and called on its attributes
    return render_template("user_profile.html", user=user)


# # THIS WORKS, but we want to use /user/<int:user_id>, which we figured out above!!
# @app.route("/user-profile")
# def user_profile():
#     """Show user information"""

#     # import pdb; pdb.set_trace()

#     # Get user email to query in User database and get all info about the user
#     email = session["logged_in_user_email"]
#     user = User.query.filter(User.email == email).one()

#     # # Test code to see attributes of user object
#     # user_id = user.user_id
#     # age = user.age
#     # zipcode = user.zipcode

#     return render_template("user_profile.html", user=user)


@app.route("/signup-login", methods=["GET"])
def show_forms():
    """Show signup and login forms."""

    return render_template("signup_login.html")


@app.route("/signup", methods=["POST"])
def signup():
    """Check if user exists in database, otherwise add user to database."""

    # Get values from signup form
    signup_email = request.form.get("signup_email")
    signup_password = request.form.get("signup_password")

    # If user exists, ask them to log in
    # Otherwise, add user into database and log them in, redirecting to homepage
    if db.session.query(User).filter(User.email == signup_email).first():
        flash("You already have an account please use login!")
        return redirect("/signup-login")

    else:
        db.session.add(User(email= signup_email, password = signup_password))
        db.session.commit()
        
        session["logged_in_user_email"] = signup_email
        
        flash("Your account has been created! You now are logged in!")
       
        return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    """Check if user's email matches password, otherwise ask user to try again."""
    
    # Get values from login form
    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")

    # If user's email and password matches, log them in, redirecting them to homepage
    # Otherwise, ask them to log in with the correct password
    if db.session.query(User).filter(User.email == login_email, 
                                     User.password == login_password).first():
        
        session["logged_in_user_email"] = login_email
        
        flash("Login SUCCESS.")        

        # Query to get user's user id, in order to redirect user to their user profile
        user = User.query.filter(User.email == login_email).one()
        user_id = user.user_id

        # Pass a variable through a string via string formatting
        # so we can pass user_id into the redirected route, which is a string!!
        return redirect("/users/%s" % user_id)
        # return redirect("/")

    else:
        flash("Incorrect password. Please try again!")
        return redirect("/signup-login")


@app.route("/logout")
def process_logout():
    """Log user out."""

    del session["logged_in_user_email"]
    
    flash("Logged out.")
    
    return redirect("/")


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    # sort movie titles alphbetically
    movies = Movie.query.order_by(Movie.title).all()
    
    return render_template("movie_list.html", movies=movies)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
