"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from sqlalchemy import func
from model import User
from model import Rating
from model import Movie
import datetime
from model import connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for row in open("seed_data/u.user"):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(user_id=user_id,
                    age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    # import pdb; pdb.set_trace()

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate movies
    Movie.query.delete()

    # Read u.item file and insert data
    for row in open("seed_data/u.item"):
        row = row.rstrip()

        movie_info = row.split("|")

        # Get information on movie_id, title, release_at, imdb_url
        movie_id = movie_info[0]
        title = movie_info[1]

        # Remove white space at end of string
        # Then remove last six characterss for year and parentheses
        title = title.rstrip() 
        title = title.rstrip(title[-6:])
        # or do title = title[:-7]

        released_str = movie_info[2]

        # Convert string to datetime object
        if released_str:
            released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        else:
            released_at = None

        imdb_url = movie_info[4]

        
        # print released_at
        # print movie_id, title

        movie = Movie(movie_id=movie_id,
                      title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        db.session.add(movie)

    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate ratings by same user
    Rating.query.delete()

    # NO NEED FOR MANUAL INCREMENTATION DUE TO AUTOINCREMENT IN MODEL
    # PSUEDO CODE for rating_id
    # total rows = 0
    # loop through file, and for each row, add to total rows
    # assign rating_id based on row # (see code in function below)
    # total_rows = 0

    # Read u.data file and insert data
    for row in open("seed_data/u.data"):
        row = row.rstrip()


        movie_id, user_id, score, timestamp = row.split("\t")
        # print movie_id, user_id, score, timestamp

        # NO NEED FOR AUTOINCREMENT
        # Increment total_rows by 1 based on each row that is looped on
        # total_rows += 1

        # For each row, assign rating_id to row number (= total_rows)
        # rating_id = total_rows

        # NO NEED TO PASS THROUGH RATING_ID
        # rating = Rating(rating_id=rating_id,
        #                 movie_id=movie_id,
        #                 user_id=user_id,
        #                 score=score)

        # No need to pass through rating_id into the object
        # as model class autoincrements this field
        # Above two functions pass through id as the id's are provided in the data
        # But the above two functions' models still autoincrement so that new data 
        # added autoincrements accordingly
        rating = Rating(movie_id=movie_id,
                        user_id=user_id,
                        score=score)

        db.session.add(rating)

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()
