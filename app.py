import json

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from sqlalchemy import ForeignKey, desc, func, create_engine
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Q:/react_apps/flask/flaskProject_lesson17/test.db'
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

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
    id = db.Column(db.Integer,ForeignKey("movies.genre_ids"),primary_key=True)#
    genre_name = db.Column(db.String)
    movie = relationship('Movies')

### Шаг 2
# Напишите сериализацию модели `Movie`.

class MoviesSchema(Schema):
    video = fields.String()
    vote_average = fields.Float()
    overview = fields.String()
    release_date = fields.String()
    vote_count = fields.Integer()
    adult = fields.String()
    backdrop_path = fields.String()
    title = fields.String()
    genre_ids = fields.Integer()
    id = fields.Integer()
    origin_country = fields.String()
    first_air_date = fields.String()
    original_language = fields.String()
    original_title = fields.String()
    poster_path = fields.String()
    popularity = fields.Float()
    media_type = fields.String()
    ######  Сколько же я потратил времени на то, чтобы допереть, что сюда нужно добавить следующее поле
    genre_name = fields.String()

class GenresSchema(Schema):
    id = fields.Integer()
    genre_name = fields.String()

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)
genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)




db.drop_all()
db.create_all()

def fill_db(class_name, json_file):
    with open(json_file, 'r', encoding='utf-8') as movies_json:
        movies_list = json.load(movies_json)
        for i in range(len(movies_list)):
            if Movies.query.get(movies_list[i].get('id')) is None:
                matrix = class_name(
                video =movies_list[i].get('video'),
                vote_average =movies_list[i].get('vote_average'),
                overview =movies_list[i].get('overview'),
                release_date =movies_list[i].get('release_date'),
                vote_count =movies_list[i].get('vote_count'),
                adult =movies_list[i].get('adult'),
                backdrop_path =movies_list[i].get('backdrop_path'),
                title =movies_list[i].get('title') or movies_list[i].get('name'),
                genre_ids =movies_list[i].get('genre_ids')[0] if movies_list[i].get('genre_ids') is not None else None,
                id =movies_list[i].get('id'),
                origin_country =movies_list[i].get('origin_country')[0] if movies_list[i].get('origin_country') is not None else None,
                first_air_date =movies_list[i].get('first_air_date'),
                original_language =movies_list[i].get('original_language'),
                original_title =movies_list[i].get('original_title'),
                poster_path =movies_list[i].get('poster_path'),
                popularity =movies_list[i].get('popularity'),
                media_type =movies_list[i].get('media_type')
                )
                db.session.add(matrix)
                del matrix
            db.session.commit()

def fill_db_simple(class_name, json_file):
    with open(json_file, 'r', encoding='utf-8') as users_js:
        users_dict = json.load(users_js)
        for i in range(len(users_dict)):
            if Genres.query.get(users_dict[i].get('id')) is None:
                john = class_name(id = users_dict[i].get('id'),genre_name = users_dict[i].get('name'))
                db.session.add(john)
                del john
            db.session.commit()

fill_db(Movies, 'movies.json')
fill_db_simple(Genres,'genres.json')

api = Api(app)
movies_route = api.namespace('movies')
genres_route = api.namespace('genres')

@app.route('/')
def hello_world():
    return 'Hello World!'

### Шаг 2
# Установите Flask-RESTX, создайте CBV для обработки GET-запроса.
# Напишите сериализацию модели `Movie`.
# Установите Flask-RESTX, создайте CBV для обработки GET-запроса.
# Доработайте представление так, чтобы оно возвращало только фильмы с определенным НАЗВАНИЕМ по запросу типа `/movies/?title=1`.
# Доработайте представление так, чтобы оно возвращало только фильмы с определенным НАЗВАНИЕМ и жанром по запросу типа /movies/?title=green&genre=12.
@movies_route.route('/')
class Movies_route(Resource):
    def get(self):
        # http://127.0.0.1:5000/movies/?genre=12&title=green get all movies in genre "action" (like condition) with title like "green"
        all_movies = db.session.query(Movies.id, Movies.title, Movies.genre_ids, Genres.genre_name.label('genre_name'),
                                          Movies.release_date).outerjoin(Genres, Movies.genre_ids==Genres.id, isouter=True).filter(Movies.title.like('%{0}%'.format(request.args.get('title') if request.args.get('title') is not None else '')),
                                                                                   (Movies.genre_ids == request.args.get('genre') if request.args.get('genre') is not None else 1==1)
                                                                                   ).order_by(desc(Movies.release_date)).all()

        # Test create_engine
        # dd = create_engine(r'sqlite:///Q:\react_apps\flask\flaskProject_lesson17\test.db')
        # sql_text = ('''select t1.title, substr(t2.genre_name,1,2) , t1.genre_ids, t2.id
        # from movies t1
        # left join genres t2 on t1.genre_ids=t2.id''')
        #
        # all_movies = dd.execute(sql_text).fetchall()
        return movies_schema.dump(all_movies),200

    def post(self):
        movies_temp = request.data#.to_dict()
        movies_list = json.loads(movies_temp.decode('utf-8'))

        # Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/movies/
        # Accept: * / *
        # Cache - Control: no - cache
        #
        # {"video": false, "vote_average": 7.0,
        #  "overview": "A dysfunctional couple head to a remote lakeside cabin under the guise of reconnecting, but each has secret designs to kill the other. Before they can carry out their respective plans, unexpected visitors arrive and the couple is faced with a greater danger than anything they could have plotted.",
        #  "release_date": "2021-07-30", "vote_count": 84, "adult": false,
        #  "backdrop_path": "/1yJ8wBmWyEM24UFUSDaRHJFMPPL.jpg", "title": "The Trip", "genre_ids": [28, 35, 53, 27],
        #  "id": 760747, "original_language": "no", "original_title": "I onde dager",
        #  "poster_path": "/uXGoV9IgKChvN7UGMj01y3purGc.jpg", "popularity": 1283.786, "media_type": "movie"}

        new_movie = Movies(
                video =movies_list.get('video'),
                vote_average =movies_list.get('vote_average'),
                overview =movies_list.get('overview'),
                release_date =movies_list.get('release_date'),
                vote_count =movies_list.get('vote_count'),
                adult =movies_list.get('adult'),
                backdrop_path =movies_list.get('backdrop_path'),
                title =movies_list.get('title') or movies_list.get('name'),
                genre_ids =movies_list.get('genre_ids')[0] if movies_list.get('genre_ids') is not None else None,
                id =movies_list.get('id'),
                # name =ies_list[i].get('name'),
                # original_name =ies_list[i].get('original_name'),
                # origin_country =e if movies_list[i].get('origin_country',None) is None else movies_list[i].get('origin_country')[0],
                origin_country =movies_list.get('origin_country')[0] if movies_list.get('origin_country') is not None else None,
                first_air_date =movies_list.get('first_air_date'),
                original_language =movies_list.get('original_language'),
                original_title =movies_list.get('original_title'),
                poster_path =movies_list.get('poster_path'),
                popularity =movies_list.get('popularity'),
                media_type =movies_list.get('media_type')
                )
        with db.session.begin():
            db.session.add(new_movie)
        return "",201

### Шаг 2
# - `/movies/<id>` — возвращает подробную информацию о фильме.
@movies_route.route('/<int:mid>')
class Movie_route(Resource):
    def get(self,mid):
        movie_container = Movies.query.get(mid)
        if movie_container is not None:
            return movie_schema.dump(movie_container),200
        else:
            return "incorrect id",404
    
    def post(self,mid:int):
        movie_to_change = Movies.query.get(mid)
        new_movie_parameters = json.loads(request.data.decode('utf-8'))

        # Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/movies/642684
        # Accept: */*
        # Cache - Control: no - cache
        #
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
        movie_to_change.genre_ids = new_movie_parameters.get('genre_ids')[0] if new_movie_parameters.get('genre_ids') is not None else None
        movie_to_change.id = new_movie_parameters.get('id')
        movie_to_change.origin_country = new_movie_parameters.get('origin_country')[0] if new_movie_parameters.get('origin_country') is not None else None
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
class Genres_route(Resource):
    def get(self):
        genres_list = Genres.query.order_by(Genres.genre_name).all()
        return genres_schema.dump(genres_list), 200

    def post(self):
        genre_for_change = json.loads(request.data.decode('utf-8'))

        # Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/genres/
        # Accept: */*
        # Cache - Control: no - cache
        #
        # {"id": 13, "genre_name": "Second"}

        new_genre = Genres(id=genre_for_change['id'], genre_name = genre_for_change['genre_name'])
        db.session.add(new_genre)
        db.session.commit()
        return "Success", 201

@genres_route.route('/<int:uid>')
class Genre_route(Resource):
    def get(self,uid):
        genre_ = Genres.query.get(uid)
        if genre_ is not None:
            return genres_schema.dump(genre_),200
        else:
            return "incorrect id",404

    def post(self,uid: int):
        genre_ = Genres.query.get(uid)
        genre_for_change = json.loads(request.data.decode('utf-8'))

        #Проверенный рабочий запрос
        # POST http://127.0.0.1:5000/genres/12
        # Accept: */*
        # Cache - Control: no - cache
        #
        # {"id": 12, "genre_name": "Second"}

        genre_.id=genre_for_change['id']
        genre_.genre_name = genre_for_change['genre_name']
        db.session.add(genre_)
        db.session.commit()
        return "Success", 201


if __name__ == '__main__':
    app.run()
