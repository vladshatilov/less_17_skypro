from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from components.db import db


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
    genre_ids = db.Column(db.Integer)
    id = db.Column(db.Integer, primary_key=True)
    origin_country = db.Column(db.String)
    first_air_date = db.Column(db.String)
    original_language = db.Column(db.String)
    original_title = db.Column(db.String)
    poster_path = db.Column(db.String)
    popularity = db.Column(db.Float)
    media_type = db.Column(db.String)


class Genres(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, ForeignKey("movies.genre_ids"), primary_key=True)
    genre_name = db.Column(db.String)
    movie = relationship('Movies')
