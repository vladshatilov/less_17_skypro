import json

def fill_db(class_name, json_file,db):
    with open(json_file, 'r', encoding='utf-8') as movies_json:
        movies_list = json.load(movies_json)
        for i in range(len(movies_list)):
            if class_name.query.get(movies_list[i].get('id')) is None:
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


def fill_db_simple(class_name, json_file,db):
    with open(json_file, 'r', encoding='utf-8') as users_js:
        users_dict = json.load(users_js)
        for i in range(len(users_dict)):
            if class_name.query.get(users_dict[i].get('id')) is None:
                john = class_name(id = users_dict[i].get('id'),genre_name = users_dict[i].get('name'))
                db.session.add(john)
                del john
            db.session.commit()