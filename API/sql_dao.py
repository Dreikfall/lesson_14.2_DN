import sqlite3
from sqlite3 import OperationalError
import json


class RequestSQL:

    def __init__(self, path="netflix.db"):
        self.path = path

    def search_title(self, name):
        """
        По вхождению name в названии фильма, находим самый новый
        :param name: str
        :return: dict
        """

        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            query = f"""
                    SELECT *
                    FROM netflix
                    WHERE title LIKE '%{name}%'        
                """
            cur.execute(query)
            executed_query = cur.fetchall()
            release_year = 0
            film = ()
            for query in executed_query: # перебираем запрос и ищем самый новый фильм
                if query[7] >= release_year:
                    film = query
                    release_year = query[7]
            try:
                dict_film = {
                    "title": film[2],
                    "country": film[5],
                    "release_year": film[7],
                    "genre": film[11],
                    "description": film[12][:-1]
                }
            except IndexError:
                return "Фильм в базе не найден(("
            return dict_film

    def movie_between(self, init_year, end_year):
        """
        Возвращает список фильмов в заданном диапазоне
        :param init_year: int or str
        :param end_year: int or str
        :return: list
        """

        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            query = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {init_year} AND {end_year}
                    ORDER BY release_year
                    LIMIT 100
            """
            try:
                cur.execute(query)
            except OperationalError:
                return "Неккоректные данные"
            executed_query = cur.fetchall()
            list_movie = []
            for _ in executed_query:
                list_movie.append({"title": _[0], "release_year": _[1]})
            if not list_movie:
                return "Выбран неверный диапазон"
            return list_movie

    def movie_rating(self, rating):
        """
        Возвращает список фильмов с заданной категорией рейтинга(children, family, adult)
        :param rating: str
        :return: list
        """
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            query = f"""
                    SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN ('G', 'PG', 'PG-13', 'R', 'NC-17')
                    ORDER BY rating       
            """
            cur.execute(query)
            executed_query = cur.fetchall()
            list_movie = []
            for _ in executed_query: #пополняем список в зависимости от выбранной категории
                if rating.lower() == "children" and _[1] in 'G':
                    list_movie.append({"title": _[0], "rating": _[1], "description": _[2]})
                elif rating.lower() == "family" and _[1] in ('G', 'PG', 'PG-13'):
                    list_movie.append({"title": _[0], "rating": _[1], "description": _[2]})
                elif rating.lower() == "adult" and _[1] in ('R', 'NC-17'):
                    list_movie.append({"title": _[0], "rating": _[1], "description": _[2]})
            if not list_movie:
                return "Выбран неверный рейтинг"
            return list_movie

    def movie_genre(self, genre):
        """Список из 10ти фильмов по совпадению с жанром

        :param genre: str
        :return: list
        """
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year
                    LIMIT 10      
            """
            cur.execute(query)
            executed_query = cur.fetchall()
            list_movie = []
            for _ in executed_query:
                list_movie.append({"title": _[0], "description": _[1]})
            if not list_movie:
                return "Задан неизвестный жанр"
            elif len(genre) < 3:
                return "Введите не менее 3 букв в строке поиска"
            return list_movie

    def two_actors(self, first="Jack Black", second="Dustin Hoffman"):
        """Список актеров, игравших с парой заданных актеров более 2 раз

        :param first: str
        :param second: str
        :return: list
        """
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            query = f"""
                    SELECT `cast`
                    FROM netflix
                    WHERE `cast` LIKE '%{first}%'
                    AND `cast` LIKE '%{second}%'
            """
            cur.execute(query)
            executed_query = cur.fetchall()
            full_actors_movie = []
            for _ in executed_query:
                full_actors_movie += _[0].split(", ") #добавляем ВСЕХ актеров из всех фильмов, игравших с first/second
            unique_list = []
            for _ in full_actors_movie:
                if full_actors_movie.count(_) > 2 and _ not in (first, second):
                    unique_list.append(_) #добавляем актеров len>2 и которые не являются first/second
            return list(set(unique_list)) #отсеиваем повторы

    def movie_to_json(self, type_movie, release_year, genre):
        """Возвращается json из фильмов с названием и описанием, исходя из заданных параметров

        :param type_movie: str
        :param release_year: int
        :param genre: str
        :return: json
        """
        if type(genre) != str or len(genre) < 3:
            return "Введите в параметре genre не менее 3 символов или введены не строчные символы"
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE type = '{type_movie}'
                    AND release_year = '{release_year}'
                    AND listed_in LIKE '%{genre}%'
                    
            """
            cur.execute(query)
            executed_query = cur.fetchall()
            list_movie = []
            for _ in executed_query:
                list_movie.append({"title": _[0], "description": _[1]})
            if not list_movie:
                return "Введены неккоретные данные"
            json_data = json.dumps(list_movie, ensure_ascii=False, indent=2)
            return json_data
