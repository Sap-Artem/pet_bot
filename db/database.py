import sqlite3


class BotDataBase:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def add(self, name='', rating=0, description='', summary='', theme='', language='', people=0, time=0, level=0,
            technologies=''):
        language = self.get_language_id(language)
        theme = self.get_theme_id(theme)
        query = """ INSERT INTO ideas
                (NAME, RATING, DESCRIPTION, SUMMARY, theme_id, LANGUAGE_ID, people_id, time_id, level_id, technologies)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?) """
        self.cursor.execute(query,
                            (name, rating, description, summary, theme, language, people, time, level, technologies))
        self.db.commit()

    def delete(self, id):
        """
        Метод удаляет идею из БД по ID.
        :param id: ID удаляемой идеи.
        """
        query = f""" DELETE FROM IDEAS WHERE IDEAS.ID={id}; """
        self.cursor.execute(query)
        self.db.commit()

    def clear(self):
        """
        ОСТОРОЖНО! Метод стирает все данные из БД. (Для тестов, потом удалю)
        """
        query = """ DELETE FROM IDEAS; """
        self.cursor.execute(query)
        self.db.commit()

    def search_by_language(self, request):
        """
        Метод принимает язык программирования и выводит краткую информацию о всех идеях с этим языком программирования из БД.
        :param request:
        :return: Список из id, name, summary каждой идеи.
        """
        request = request.split(': ')[1]
        query = f''' SELECT ideas.id, ideas.name, ideas.summary, language_name FROM ideas JOIN languages ON languages.language_id = ideas.language_id WHERE language_name="{request}";  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def search_by_people(self, request: str):
        """
        Метод принимает кол-во участников и выводит краткую информацию о всех идеях с этим кол-вом участников из БД.
        :param request: Кол-во участников, как на кнопке.
        :return: Список из id, name, summary каждой идеи.
        """
        query = f'''    SELECT ideas.id, ideas.name, ideas.summary, people.people_id FROM IDEAS
                                INNER JOIN people ON people.people_id = ideas.people_id
                                WHERE people_name="{request}";  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def search_by_format(self, request: str):
        request = request.split('-')[0]
        """
        Метод принимает формат (тему) идеи и выводит краткую информацию о всех идеях с этим форматом из БД.
        :param request: Формат, как на кнопке.
        :return: Список из id, name, summary каждой идеи.
        """
        request = request.split('-')[0]
        query = f''' SELECT IDEAS.ID, IDEAS.NAME, IDEAS.SUMMARY FROM IDEAS JOIN themes ON themes.id = ideas.theme_id WHERE theme_name="{request}";  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def search_by_time(self, request):
        request = request.split(': ')[1]
        """
        Метод принимает срок выполнения идеи и выводит краткую информацию о всех идеях с этим сроком из БД.
        :param request: Время, как на кнопке.
        :return: Список из id, name, summary каждой идеи.
        """
        query = f'''    SELECT ideas.id, ideas.name, ideas.summary FROM IDEAS
                        WHERE ideas.time_id={self.get_time_id(request)};  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def get_by_id(self, idea_id: int):
        """
        Метод принимает ID идеи и выводит всю информацию о ней из БД.
        :param idea_id: ID
        :return: id, name, rating, description, summary, theme, language, level, technologies_id, technologies_name
        """
        query = f''' 
            SELECT ideas.name, ideas.rating, ideas.description, themes.theme_name, people.people_name, times.time_name, languages.language_name, levels.level_name, ideas.technologies FROM IDEAS
            INNER JOIN languages ON languages.language_id = ideas.language_id
            INNER JOIN themes ON themes.id = ideas.theme_id
            INNER JOIN times ON times.time_id = ideas.time_id
            INNER JOIN people ON people.people_id = ideas.people_id
            INNER JOIN levels ON levels.level_id = ideas.level_id
            WHERE IDEAS.id={idea_id}
            '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        print(response, idea_id)
        return response

    def get_all(self, n=None, reverse=False):
        """
        Метод возвращает название, краткую информацию о N-ом количестве идей из БД.
        Если n не задано, метод возвращает информацию о всех идеях.
        :param reverse: False (по умолчанию) - возвращает список в обычном порядке. True - в обратном.
        :param n: Количество возвращаемых идей. Если не задано - вернет все.
        :return: Список из id, name, summary каждой идеи.
        """
        flag_amount = ''
        flag_reverse = ''
        if n:
            flag_amount = ' LIMIT ' + str(n)
        if reverse:
            flag_reverse = ' ORDER BY id DESC '
        query = f''' SELECT id, name, summary FROM ideas{flag_reverse}{flag_amount};  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def is_admin(self, check_id: int) -> bool:
        """
        Функция проверят, содержится ли id в базе админов.
        :param check_id: Проверяемый id
        :return: True, если id админский, False, если нет.
        """
        query = ''' SELECT * FROM admins; '''
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return check_id in [item[0] for item in response]

    def get_language_id(self, item):
        """
        Функция возвращает id языка из базы по названию
        :param item: название языка
        :return: id или 0
        """
        query = f''' SELECT language_id FROM languages WHERE language_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return 0

    def get_people_id(self, item):
        """
        Функция возвращает id кол-ва людей из базы по тексту
        :param item: текст кол-ва людей
        :return: id или 0
        """
        query = f''' SELECT people_id FROM people WHERE people_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return 0

    def get_time_id(self, item):
        """
        Функция возвращает id времени из базы по тексту
        :param item: текст времени
        :return: id или 0
        """
        query = f''' SELECT time_id FROM times WHERE time_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return 0

    def get_theme_id(self, item):
        """
        Функция возвращает id формата из базы по названию
        :param item: название формата
        :return: id или 0
        """
        item = item.split('-')[0]
        query = f''' SELECT id FROM themes WHERE theme_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return 0

    def get_level_id(self, item):
        """
        Функция возвращает id уровня из базы по названию
        :param item: название уровня
        :return: id или 0
        """
        query = f''' SELECT level_id FROM levels WHERE level_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return 0

    def add_suggestion(self, name='', rating=0, description='', summary='', theme='', language='', people='', time='',
                       level='',
                       technologies=''):
        """
        Функция принимает информацию из идеи и добавляет ее в предложку
        :param name:
        :param rating:
        :param description:
        :param summary:
        :param theme:
        :param language:
        :param people:
        :param time:
        :param level:
        :param technologies:
        """
        language = self.get_language_id(language)
        theme = self.get_theme_id(theme)
        time = self.get_time_id(time)
        people = self.get_people_id(people)
        level = self.get_level_id(level)
        query = """ INSERT INTO suggestions
        (NAME, RATING, DESCRIPTION, SUMMARY, theme_id, LANGUAGE_ID, people_id, time_id, level_id, technologies)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?) """
        self.cursor.execute(query,
                            (name, rating, description, summary, theme, language, people, time, level, technologies))
        self.db.commit()

    def reject_suggestion(self, id):
        """
        Функция удаляет идею из предложки по id
        :param id:
        :return:
        """
        query = f""" DELETE FROM suggestions WHERE id={id}; """
        self.cursor.execute(query)
        self.db.commit()

    def approve_suggestion(self, id, rating: int):
        """
        Функция переносит идею из предложки в основную базу по id и добавляет к ней рейтинг от модератора.
        :param rating: Рейтинг в числовом виде от 1 до 10 от модератора.
        :param id: id идеи
        :return:
        """
        query1 = f'''INSERT INTO ideas 
        (name, rating, description, summary, theme_id, language_id, people_id, time_id, level_id, technologies)  
        SELECT name, {rating}, description, summary, theme_id, language_id, people_id, time_id, level_id, technologies
        FROM suggestions WHERE suggestions.id = {id};'''
        query2 = f'''DELETE FROM suggestions WHERE id={id}; '''
        self.cursor.execute(query1)
        self.cursor.execute(query2)
        self.db.commit()

    def get_suggestion(self):
        """
        Метод возвращает первую предложенную идею.
        :return: Вся информация об идее
        """
        query = ''' SELECT * FROM suggestions LIMIT 1;'''
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def ideas_amount(self) -> int:
        """
        Метод возвращает количество идей в БД.
        :return: Число идей в БД
        """
        query = ''' SELECT COUNT(*) FROM IDEAS; '''
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_all_suggestions(self):
        """
        Возвращает список из всех идей из предложки.
        :return:
        """
        query = f''' 
                    SELECT suggestions.name, suggestions.rating, suggestions.description, themes.theme_name, people.people_name, times.time_name, languages.language_name, levels.level_name, suggestions.technologies FROM suggestions
                    INNER JOIN languages ON languages.language_id = suggestions.language_id
                    INNER JOIN themes ON themes.id = suggestions.theme_id
                    INNER JOIN times ON times.time_id = suggestions.time_id
                    INNER JOIN people ON people.people_id = suggestions.people_id
                    INNER JOIN levels ON levels.level_id = suggestions.level_id
                '''
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def suggestions_amount(self) -> int:
        """
        Метод возвращает количество предложенных идей в БД.
        :return: Число идей в предложке
        """
        query = ''' SELECT COUNT(*) FROM suggestions; '''
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_all_languages(self):
        """
        Метод выводит все языки из базы языков программирования.
        :return: Список из языков
        """
        query = ''' SELECT language_name FROM languages; '''
        self.cursor.execute(query)
        response = []
        for element in self.cursor.fetchall():
            current = element[0]
            if current:
                response.append(current)
        return response

    def get_all_themes(self):
        """
        Метод выводит все форматы из базы форматов.
        :return: Список из форматов
        """
        query = ''' SELECT theme_name FROM themes; '''
        self.cursor.execute(query)
        response = []
        for element in self.cursor.fetchall():
            current = element[0]
            if current:
                response.append(current)
        return response

    def get_language(self, id):
        """
        Функция возвращает название языка из базы по id
        :param id:
        :return: название
        """
        query = f''' SELECT language_name FROM languages WHERE language_id={id}; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return '-'

    def get_people(self, id):
        """
        Функция возвращает кол-во людей из базы по id
        :param id:
        :return: кол-во людей
        """
        query = f''' SELECT people_name FROM people WHERE people_id={id}; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return '-'

    def get_time(self, id):
        """
        Функция возвращает название времени из базы по id
        :param id:
        :return: название
        """
        query = f''' SELECT time_name FROM times WHERE time_id={id}; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return '-'

    def get_theme(self, id):
        """
        Функция возвращает название формата из базы по id
        :param id:
        :return: название
        """
        query = f''' SELECT theme_name FROM themes WHERE id={id}; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return '-'

    def get_level(self, id):
        """
        Функция возвращает название уровня из базы по id
        :param id:
        :return: название
        """
        query = f''' SELECT level_name FROM levels WHERE level_id={id}; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        else:
            return '-'


if __name__ == "__main__":
    db = BotDataBase('database.db')
    # print(db.search_by_language('Python'))
    # print(db.search_by_language('C#; C++'))
    # print(db.get_all_languages())
    # print(db.get_all_themes())
    print(db.get_language(1))
    print(db.get_level(1))
    print(db.get_theme(1))
    print(db.get_people(1))
    print(db.get_time(1))
    # db.approve_suggestion(1, 9)
    # print(db.get_by_id(1))
    # db.add_suggestion('123', 1, '222222', '12312312312')
    # db.reject_suggestion(db.get_suggestion()[0])
    # db.add_suggestion('Тест 1', 11, 'Описание идеи', 'Краткое описание', 'Backend-разработка', 'Python', 'Меньше 3',
                      # 'Полгода', 'продвинутый', 'Технологии древних русов')
    # db.add('Классная идея 2', 8, 'Описание идеи 2', 'Краткое описание 2',
    # 'Mobile-разработка', 'JavaScript', 3, 2)
    # db.add('Классная идея 3', 7, 'Описание идеи 3', 'Краткое описание 1',
    # 'Mobile-разработка', 'Python', 3, 3)
    # print(db.search_by_language('Python'))
    # print(db.search_by_people('более 8 человек'))
    # print(db.search_by_format('Frontend-разработка'))
    # print(db.search_by_time('срок: меньше недели'))
