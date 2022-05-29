from flask import Blueprint, jsonify
from API.sql_dao import RequestSQL

api_blueprint = Blueprint("api_blueprint", __name__)


@api_blueprint.route("/movie/<title>/")
def film_data(title):
    data_film = RequestSQL().search_title(title)
    return jsonify(data_film)


@api_blueprint.route("/movie/<year_1>/to/<year_2>/")
def year_range(year_1, year_2):
    data_film = RequestSQL().movie_between(year_1, year_2)
    return jsonify(data_film)


@api_blueprint.route("/rating/<rating_group>/")
def group_rating_movie(rating_group):
    data_film = RequestSQL().movie_rating(rating_group)
    return jsonify(data_film)


@api_blueprint.route("/genre/<genre>/")
def get_movie_to_genre(genre):
    data_film = RequestSQL().movie_genre(genre)
    return jsonify(data_film)
