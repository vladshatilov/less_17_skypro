from marshmallow import Schema, fields


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
    genre_name = fields.String()


class GenresSchema(Schema):
    id = fields.Integer()
    genre_name = fields.String()
