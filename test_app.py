import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from database.models import setup_db


class CastingTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_user = 'serag'
        self.database_pass = 'password1'
        self.database_name = "casting_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            self.database_user, self.database_pass,
            'localhost:5432', self.database_name
        )

        self.new_actor = {
            'name': 'Zack',
            'age': 25,
            'gender': 'M'
        }

        self.new_movie = {
            'title': 'The Developer',
            'release_date': '20-5-2023'
        }

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # TEST CASES FOR PROCESS SUCCESS

    # 1. GET Actors
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['actors'])
        self.assertEqual(type(data['actors']), list)

    # 2. GET Movies
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # self.assertTrue(data['movies'])
        self.assertEqual(type(data['movies']), list)

    # 3. POST Actors
    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # 4. POST Movies
    def test_post_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # 5. PATCH actor
    def test_edit_actor(self):
        res = self.client().patch('/actors/2', json={'movies': 2})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    # 6. PATCH movie
    def test_edit_movie(self):
        res = self.client().patch('/movies/2', json={'title': 'Terminator'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # 7. DELETE actor
    def test_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], 1)

    # 8. DELETE movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted'], 1)

    # TEST CASES FOR PROCESS SUCCESS
    # 1. GET Actors
    # 2. GET Movies
    # 3. POST Actor
    def test_post_actor_faliure(self):
        res = self.client().post('/actors', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # 4. POST Movie
    def test_post_movie_faliure(self):
        res = self.client().post('/movies', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # 5. PATCH Actor
    def test_patch_actor_faliure(self):
        res = self.client().patch('/actors/2', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # 6. PATCH Movie
    def test_patch_movie_faliure(self):
        res = self.client().patch('/movies/2', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    # 7. DELETE Actor
    def test_delete_actor_faliure(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # 8. DELETE Movie
    def test_delete_movie_faliure(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
