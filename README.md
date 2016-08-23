# MyMovies

Find movies you love and compare your ratings with the Wizard!
Let's see what your taste in movies is like.

### Table of Contents

1. [Technologies](#technologies)
2. [Features](#features)
3. [Installation](#installation)
4. [Deployment](#deployment)
5. [Author](#author)

## <a name="technologies"></a>Technologies

**Front-end:** [HTML5](http://www.w3schools.com/html/), [CSS](http://www.w3schools.com/css/), [Bootstrap](http://getbootstrap.com), [Javascript](https://developer.mozilla.org/en-US/docs/Web/JavaScript), [jQuery](https://jquery.com/)

**Back-end:** [Python](https://www.python.org/), [Flask](http://flask.pocoo.org/), [Jinja2](http://jinja.pocoo.org/docs/dev/), [PostgreSQL](http://www.postgresql.org/), [SQLAlchemy](http://www.sqlalchemy.org/)

**Libraries:** [SQLAlchemy-Searchable](https://sqlalchemy-searchable.readthedocs.io)

**APIs:** [Omdb](http://www.omdbapi.com/)

**Data Set:** [100k MovieLens] (http://grouplens.org/datasets/movielens/100k/)

## <a name="features"></a>Features
###Landing page:
<img align="center" src="/static/images/homepic.png" width="500">

###Sign Up and Log In
<img align="center" src="/static/images/signuppic.png" width="500">

+ Users can sign up for an account
+ Users can log in if they are an existing user
+ If the user doesn’t have an account they can click on the link to sign-up and that will take them to a form where they’ll be asked to input information. 
+ When that user submits the form, the form is POSTed to a route in the server which then stores the user information in the Postgres database
+ Once a user is logged in, they are redirected to their user profile page where on the server uses SQLAlchemy to query the Postgres database to return a user object which passes the variables into the jinja template so that it could access the object's attributes to display information about the user.


###Homepage

###Movie List
+ List of Movie Profiles

<img align="center" src="/static/images/movielist.png" width="500">


###User Profile
+ User profile page allows you to rate your favorite movies to your profile for easy access later.

<img align="center" src="/static/images/userpic.png" width="500">


###Movie Profile

+
+
+

<img align="center" src="/static/imgs/moviepic.png" width="500">
## <a name="installation"></a>Installation
As MyMovies has not yet been deployed, please follow these instructions to run MyMovies locally on your machine:

### Prerequisite:

Install [PostgreSQL](http://postgresapp.com) (Mac OSX).

Postgres needs to be running in order for the app to work. It is running when you see the elephant icon:

<img align="center" src="/static/imgs/postgres.png" width="200">

Add /bin directory to your path to use PostgreSQL commands and install the Python library.

Use Sublime to edit `~/.bash_profile` or `~/.profile`, and add:

```export PATH=/Applications/Postgres.app/Contents/Versions/9.5/bin/:$PATH``` 

### Set up MyMovies:

Clone this repository:

```$ git clone https://github.com/allisonscofield/ratings.git```

Create a virtual environment and activate it:

```
$ virtualenv env
$ source env/bin/activate
```

Install the dependencies:

```$ pip install -r requirements.txt```

Run PostgreSQL (make sure elephant icon is active).

Create database with the name `ratings`.

```$ createdb ratings```

Seed the database with movies and ratings:

```$ python seed.py```

Finally, to run the app, start the server:

```$ python server.py```

Go to `localhost:5000` in your browser to start using MyMovies!

## <a name="deployment"></a>Deployment
Deployment details coming very soon!



## <a name="authoe"></a>Author  
Allison Scofield is a Software Engineer living in Southern California. <br>
[LinkedIn](https://www.linkedin.com/in/allisonscofield) | [Email](mailto:allisonscofield@gmail.com) 

Ashley Hsiao is a Software Engineer living in the San Francisco Bay Area. <br>
[Email](mailto:aiyihsiao@gmail.com) | [LinkedIn](http://linkedin.com/in/ashleyhsia0) | [Twitter](http://twitter.com/ashleyhsia0).
