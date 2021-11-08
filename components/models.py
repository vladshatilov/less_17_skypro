from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from components.db import db


movies_genres = db.Table('movies_genres',
                         # db.Column('id', autoincrement=True, primary_key=True),
                         db.Column('genre_id', db.Integer, db.ForeignKey('genres.id')),
                         db.Column('movies_id', db.Integer, db.ForeignKey('movies.id'))
                         )

class Movies(db.Model):
    __tablename__ = 'movies'
    video = db.Column(db.String)
    vote_average = db.Column(db.Float)
    overview = db.Column(db.String)
    release_date = db.Column(db.String)
    vote_count = db.Column(db.Integer)
    adult = db.Column(db.String)
    backdrop_path = db.Column(db.String)
    title = db.Column(db.String)
    # genre_ids = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    origin_country = db.Column(db.String)
    first_air_date = db.Column(db.String)
    original_language = db.Column(db.String)
    original_title = db.Column(db.String)
    poster_path = db.Column(db.String)
    popularity = db.Column(db.Float)
    media_type = db.Column(db.String)
    # genres = db.relationship('genres', secondary = movies_genres,
    #                          backref=db.backref('movies', lazy = 'dynamic'))
    genres = relationship('Genres', secondary=movies_genres, backref='Movies')


class Genres(db.Model):
    __tablename__ = 'genres'
    # id = db.Column(db.Integer, ForeignKey("movies.genre_ids"), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String)
    # movie = relationship('Movies')
    movies = relationship('Movies', secondary=movies_genres, backref='Genres')
