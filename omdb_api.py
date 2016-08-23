import requests
from model import Movie, db

OMDB_URL = "http://www.omdbapi.com/?t="


def get_movie_info():
    """Get movie information from OMDB API for all movies and update in database."""

    movies = db.session.query(Movie).all()
    # Movie.query.all()

    for movie in movies:

        response = requests.get(OMDB_URL + movie.title)

        json_response = response.json()

        movie.description = json_response.get('Plot', "")
        movie.genre = json_response.get('Genre', "")
        movie.image_url = json_response.get('Poster', "")
        movie.rated = json_response.get('Rated', "")

        db.session.commit()


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."
