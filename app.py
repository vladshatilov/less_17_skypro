import json

from flask import Flask, request, jsonify
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, desc
from sqlalchemy.orm import relationship

from components.db import db, create_app
from components.models import Movies, Genres
from components.fill_db_func import fill_db_simple, fill_db
from components.schemas import MoviesSchema, GenresSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Q:/react_apps/flask/flaskProject_lesson17/test.db'
app.config['JSON_AS_ASCII'] = False
db.init_app(app)

# drop all tables and fill them with content
with app.app_context():
    db.drop_all()
    db.create_all()
    fill_db_simple(Genres, 'genres.json', db)
    fill_db(Movies, 'movies.json', db)

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)
genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)

api = Api(app)
movies_route = api.namespace('movies')
genres_route = api.namespace('genres')


@app.route('/')
def hello_world():
    return 'Hello World!'


### Шаг 2
# Установите Flask-RESTX, создайте CBV для обработки GET-запроса.
# Напишите сериализацию модели `Movie`.
@movies_route.route('/')
class Movies_route_json(Resource):
    def get(self):
        # http://127.0.0.1:5000/movies/?genre=12&title=green get all movies in genre "action" (like condition) with title like "green"

        if request.args.get('genre') is not None:
            all_movies = db.session.query(Movies.id, Movies.title,
                                          Genres.genre_name.label('genre_name'),
                                          Movies.release_date
                                          ).join(Genres, Movies.genres).filter(
                                                Movies.title.like('%{0}%'.format(request.args.get('title') if request.args.get('title') is not None else '')),
                                                (Genres.id == request.args.get('genre') if request.args.get('genre') is not None else 1 == 1)
                                            ).order_by(desc(Movies.release_date)).all()
        else:
            all_movies = db.session.query(Movies.id, Movies.title,
                                          Movies.release_date
                                          ).filter(
                                                Movies.title.like('%{0}%'.format(request.args.get('title') if request.args.get('title') is not None else ''))
                                            ).order_by(desc(Movies.release_date)).all()

        return jsonify(movies_schema.dump(all_movies))

    def post(self):
        movies_temp = request.data  # .to_dict()
        movies_list = json.loads(movies_temp.decode('utf-8'))

        # Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/movies/
        # {"video": false, "vote_average": 7.0,
        #          "overview": "A dysfunctional couple",
        #          "release_date": "2021-07-30", "vote_count": 84, "adult": false,
        #          "backdrop_path": "/1yJ8wBmWyEM24UFUSDaRHJFMPPL.jpg", "title": "The Ptica", "genre_ids": [12, 14, 53, 27],
        #          "id": 12, "original_language": "no", "original_title": "I onde dager",
        #          "poster_path": "/uXGoV9IgKChvN7UGMj01y3purGc.jpg", "popularity": 1283.786, "media_type": "movie"}
        print(movies_list)
        new_movie = Movies(
            video=movies_list.get('video'),
            vote_average=movies_list.get('vote_average'),
            overview=movies_list.get('overview'),
            release_date=movies_list.get('release_date'),
            vote_count=movies_list.get('vote_count'),
            adult=movies_list.get('adult'),
            backdrop_path=movies_list.get('backdrop_path'),
            title=movies_list.get('title') or movies_list.get('name'),
            # genre_ids=movies_list.get('genre_ids')[0] if movies_list.get('genre_ids') is not None else None,
            id=movies_list.get('id'),
            origin_country=movies_list.get('origin_country')[0] if movies_list.get(
                'origin_country') is not None else None,
            first_air_date=movies_list.get('first_air_date'),
            original_language=movies_list.get('original_language'),
            original_title=movies_list.get('original_title'),
            poster_path=movies_list.get('poster_path'),
            popularity=movies_list.get('popularity'),
            media_type=movies_list.get('media_type')
        )
        if movies_list.get('genre_ids') is not None:
            for i in movies_list.get('genre_ids'):
                c1 = Genres.query.get(i)
                new_movie.genres.append(c1)
                db.session.add(new_movie)
                db.session.commit()
        with db.session.begin():
            db.session.add(new_movie)
        return "", 201


### Шаг 2
# - `/movies/<id>` — возвращает подробную информацию о фильме.
@movies_route.route('/<int:mid>')
class Movie_route_json(Resource):
    def get(self, mid):
        movie_container = Movies.query.get(mid)
        if movie_container is not None:
            return jsonify(movie_schema.dump(movie_container))
        else:
            return "incorrect id", 404

    def post(self, mid: int):
        movie_to_change = Movies.query.get(mid)
        new_movie_parameters = json.loads(request.data.decode('utf-8'))

        # Проверенный запрос
        # POST http://127.0.0.1:5000/movies/642684
        # {"adult": true, "backdrop_path": "/cthCF9Me0LViWbKYTd06DKm9WIH.jpg", "vote_count": 224,
        #  "original_language": "fr", "original_title": "OpérationPortugal",
        #  "poster_path": "/dnR42jxXOWmwrBsn1S9AWRnWNGB.jpg", "release_date": "2021-06-23", "video": false,
        #  "vote_average": 5.0, "title": "OpérationPortugal",
        #  "overview": "Hakim,35,afriendlyneighborhoodcop,mustinfiltratethePortuguesecommunityforthepurposeofaninvestigation.ButcanonebecomePortugueseinthreedays?EspeciallywhenweknowthatHakimisawalkingdisasteratundercoveroperations.Hisclumsinessandbadluckturnhismanyinfiltrationsintocataclysms.Thecaseisclearlytoobigforhim.Quicklytrappedbetweenhisfeelingsandhismission,Hakim,wholivesalonewithhismother,willdiscoveracommunity,butalsoafamily.",
        #  "id": 642684, "popularity": 68.953, "media_type": "movie"}

        movie_to_change.video = new_movie_parameters.get('video')
        movie_to_change.vote_average = new_movie_parameters.get('vote_average')
        movie_to_change.overview = new_movie_parameters.get('overview')
        movie_to_change.release_date = new_movie_parameters.get('release_date')
        movie_to_change.vote_count = new_movie_parameters.get('vote_count')
        movie_to_change.adult = new_movie_parameters.get('adult')
        movie_to_change.backdrop_path = new_movie_parameters.get('backdrop_path')
        movie_to_change.title = new_movie_parameters.get('title') or new_movie_parameters.get('name')
        # movie_to_change.genre_ids = new_movie_parameters.get('genre_ids')[0] if new_movie_parameters.get(
        #     'genre_ids') is not None else None
        movie_to_change.id = new_movie_parameters.get('id')
        movie_to_change.origin_country = new_movie_parameters.get('origin_country')[0] if new_movie_parameters.get(
            'origin_country') is not None else None
        movie_to_change.first_air_date = new_movie_parameters.get('first_air_date')
        movie_to_change.original_language = new_movie_parameters.get('original_language')
        movie_to_change.original_title = new_movie_parameters.get('original_title')
        movie_to_change.poster_path = new_movie_parameters.get('poster_path')
        movie_to_change.popularity = new_movie_parameters.get('popularity')
        movie_to_change.media_type = new_movie_parameters.get('media_type')

        db.session.add(movie_to_change)
        db.session.commit()
        return "", 201


@genres_route.route('/')
class Genres_route_json(Resource):
    def get(self):
        genres_list = Genres.query.order_by(Genres.genre_name).all()
        return jsonify(genres_schema.dump(genres_list))

    def post(self):
        genre_for_change = json.loads(request.data.decode('utf-8'))

        # Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/genres/
        # {"id": 13, "genre_name": "Second"}

        new_genre = Genres(id=genre_for_change['id'], genre_name=genre_for_change['genre_name'])
        db.session.add(new_genre)
        db.session.commit()
        return "Success", 201


@genres_route.route('/<int:uid>')
class Genre_route_json(Resource):
    def get(self, uid):
        genre_ = Genres.query.get(uid)
        if genre_ is not None:
            return jsonify(genre_schema.dump(genre_))
        else:
            return "incorrect id", 404

    def post(self, uid: int):
        genre_ = Genres.query.get(uid)
        genre_for_change = json.loads(request.data.decode('utf-8'))

        # Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/genres/12
        # {"id": 12, "genre_name": "Second"}

        genre_.id = genre_for_change['id']
        genre_.genre_name = genre_for_change['genre_name']
        db.session.add(genre_)
        db.session.commit()
        return "Success", 201


if __name__ == '__main__':
    app.run()
