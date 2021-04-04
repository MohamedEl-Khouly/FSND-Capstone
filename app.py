# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from database.models import setup_db, Actor, Movie
#from auth.auth import AuthError, requires_auth

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
        return jsonify({
            'url': 'Login Url'
        })

#  Actors
#  ----------------------------------------------------------------

        # GET
    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        if actors is None:
            abort(404)
        formated_actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': formated_actors
        })
        # POST

    @app.route('/actors', methods=['POST'])
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
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        if movies is None:
            abort(404)
        formated_movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': formated_movies
        })

        # POST
    @app.route('/movies', methods=["POST"])
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

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
