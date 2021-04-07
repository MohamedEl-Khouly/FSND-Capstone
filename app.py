# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth

# ----------------------------------------------------------------------------#
# Constants & Helper methods
# ----------------------------------------------------------------------------#
ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE'))
DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUDIENCE = os.environ.get('API_AUDIENCE')
CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
CALLBACK_URI = os.environ.get('AUTH0_CALLBACK_URL')


def paginate(request, selection):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    return selection[start:end]

# ----------------------------------------------------------------------------#
# Create & Configure App
# ----------------------------------------------------------------------------#


def create_app(test_config=None):
    # ----------------------------------------------------------------------------#
    #  Setup.
    # ----------------------------------------------------------------------------#
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Intiate CORS
    CORS(app)

    # After request headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response


# ----------------------------------------------------------------------------#
# Routes.
# ----------------------------------------------------------------------------#
#  Basic
#  ----------------------------------------------------------------

    # Index

    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            'success': True,
            'App': 'Casting Agency'
        })

        # Auth
    @app.route('/auth', methods=['GET'])
    def authentication_request():
        url = f'https://${DOMAIN}/authorize?audience=${AUDIENCE}&response_type=token&client_id=${CLIENT_ID}&redirect_uri=${CALLBACK_URI}'
        return jsonify({
            'url': url
        })

#  Actors
#  ----------------------------------------------------------------

    # GET
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        if actors is None:
            abort(404)
        current_actors = paginate(request, actors)
        formated_actors = [actor.format() for actor in current_actors]
        return jsonify({
            'success': True,
            'actors': formated_actors,
            'total_actors': len(actors)
        })
        # POST

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def new_actor():
        body = request.get_json()
        if not('name' in body and 'age' in body and 'gender' in body):
            abort(400)
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        if name is None or age is None or gender is None:
            abort(422)
        actor = Actor(name=name, age=age, gender=gender)
        actor.insert()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

        # PATCH
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        body = request.get_json()
        if not('name' in body or 'age' in body or 'gender' in body or 'movies' in body):
            abort(400)

        if 'name' in body:
            name = body.get('name', None)
            if name is None:
                abort(422)
            actor.name = name
        if 'age' in body:
            age = body.get('age', None)
            if age is None:
                abort(422)
            actor.age = age
        if 'gender' in body:
            gender = body.get('gender', None)
            if gender is None:
                abort(422)
            actor.gender = gender
        if 'movies' in body:
            movie_id = body.get('movies', None)
            if movie_id is None:
                abort(422)
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(400)
            actor.movies.append(movie)
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        })

        # DELETE
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor_id
        })


#  Movies
#  ----------------------------------------------------------------

        # GET


    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        if movies is None:
            abort(404)
        current_movies = paginate(request, movies)
        formated_movies = [movie.format() for movie in current_movies]
        return jsonify({
            'success': True,
            'movies': formated_movies,
            'total_movies': len(movies)
        })

        # POST
    @app.route('/movies', methods=["POST"])
    @requires_auth('post:movies')
    def new_movie():
        body = request.get_json()
        if not('title' in body and 'release_date' in body):
            abort(400)
        title = body.get('title')
        release_date = body.get('release_date')
        movie = Movie(title=title, release_date=release_date)
        movie.insert()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })
        # PATCH

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        body = request.get_json()

        if not('title' in body or 'release_date' in body or 'actors' in body):
            abort(400)

        if ('title' in body):
            title = body.get('title', None)
            if title is None:
                abort(422)
            movie.title = title
        if ('release_date' in body):
            release_date = body.get('release_date', None)
            if release_date is None:
                abort(422)
            movie.release_date = release_date
        if ('actors' in body):
            actor_id = body.get('actors')
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(400)
            movie.actors.append(actor)
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        })

        # DELETE
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })


# ----------------------------------------------------------------------------#
# Error Handlers.
# ----------------------------------------------------------------------------#
    # 1. 400

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "BAD REQUEST"
        }), 400
    # 2. 404

    @app.errorhandler(404)
    def ressource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "RESSOURCE NOT FOUND"
        }), 404

    # 3. 422
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "REQUEST UNPROCESSABLE"
        }), 422

    # 4. AuthError
    @app.errorhandler(AuthError)
    def authentication_failed(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            "description": error.error['description'],
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
