# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import os
from sqlalchemy import (
    Column, String,
    Integer, DateTime,
    Enum, ForeignKey
)
from sqlalchemy.schema import Table
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ----------------------------------------------------------------------------#
# Setup.
# ----------------------------------------------------------------------------#
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

#  Association table
#  ----------------------------------------------------------------
movie_actors = Table(
    'movie_actors',
    db.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True)
)


#  Actors Model
#  ----------------------------------------------------------------
class Actor(db.Model):
    __tablename__ = 'actors'

    # Table Columns
    id = Column(Integer, primary_key=True)
    name = Column(String(), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('M', 'F',  name='gender_types'))

    # Model functions
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f'< {self.id}: {self.name}, {self.age}, {self.gender}>'
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.title for movie in self.movies]
        }


#  Movies Model
#  ----------------------------------------------------------------
class Movie(db.Model):
    __tablename__ = 'movies'

    # Table Columns
    id = Column(Integer, primary_key=True)
    title = Column(String(), nullable=False)
    release_date = Column(DateTime)

    # relation
    actors = relationship(
        'Actor', secondary=movie_actors,
        backref=backref('movies', lazy=True)
    )

    # Model functions
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f'<{self.id}: {self.title}, {self.release_date}>'

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]
        }
