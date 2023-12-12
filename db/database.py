import sqlite3


class BotDataBase:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()

    def add(self, name='', rating=0, description='', summary='', theme='', language='', people=0, time=0, level=0,
            technologies=''):
        query = """ INSERT INTO IDEAS
        (NAME, RATING, DESCRIPTION, SUMMARY, THEME, LANGUAGE_ID, PEOPLE, TIME, LEVEL, TECHNOLOGIES_ID)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?) """
        self.cursor.execute(query,
                            (name, rating, description, summary, theme, language, people, time, level, technologies))
        self.db.commit()

    def update(self, id, name, rating, description, summary, theme, language, level, technologies):
        pass

    def get(self):
        query = """ SELECT IDEAS.*, TECHNOLOGIES.NAME FROM IDEAS, TECHNOLOGIES WHERE IDEAS.TECHNOLOGIES=TECHNOLOGIES.id; """
        self.cursor.execute(query)
        for res in self.cursor:
            print(res)

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

    def search_by_language(self, lang_str):
        print(lang_str)
        """
        Метод принимает язык программирования и выводит краткую информацию о всех идеях с этим языком программирования из БД.
        :param lang_str:
        :return: Список из id, name, summary каждой идеи.
        """
        if ';' in lang_str:
            languages = lang_str.split('; ')
        else:
            languages = [lang_str]
        response = []
        for language in languages:
            query = f''' SELECT ideas.id, ideas.name, ideas.summary, language_name FROM ideas JOIN languages ON languages.language_id = ideas.language_id WHERE language_name="{language}";  '''
            self.cursor.execute(query)
            response += [res for res in self.cursor]
        return response

    def search_by_people(self, people_number: str):
        """
        Метод принимает кол-во участников и выводит краткую информацию о всех идеях с этим кол-вом участников из БД.
        :param people_number: Кол-во участников, как на кнопке.
        :return: Список из id, name, summary каждой идеи.
        """
        if people_number == "1 человек":
            request = '=1'
        elif people_number == "2 человека":
            request = '=2'
        elif people_number == "3-8 человек":
            request = ' >2 AND IDEAS.PEOPLE < 9'
        elif people_number == "более 8 человек":
            request = '>8'
        query = f''' SELECT IDEAS.ID, IDEAS.NAME, IDEAS.SUMMARY FROM IDEAS WHERE IDEAS.PEOPLE{request};  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def search_by_format(self, request: str):
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

    def search_by_time(self, time: str):
        """
        Метод принимает срок выполнения идеи и выводит краткую информацию о всех идеях с этим сроком из БД.
        :param time: Время, как на кнопке.
        :return: Список из id, name, summary каждой идеи.
        """
        if time == "срок: меньше недели":
            request = '<7'
        elif time == "срок: от недели до месяца":
            request = ' >6 AND IDEAS.time < 32'
        elif time == "срок: от месяца до полугода":
            request = ' >31 AND IDEAS.time < 183'
        elif time == "срок: более полугода":
            request = '>182'
        query = f''' SELECT IDEAS.ID, IDEAS.NAME, IDEAS.SUMMARY FROM IDEAS WHERE IDEAS.time{request};  '''
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
            SELECT ideas.name, ideas.rating, ideas.description, themes.theme_name, ideas.people, ideas.time, languages.language_name, ideas.level, technologies.name FROM IDEAS
            INNER JOIN languages ON languages.language_id = ideas.language_id
            INNER JOIN themes ON themes.id = ideas.theme_id
            INNER JOIN technologies ON technologies.id = ideas.technologies_id
            WHERE IDEAS.id={idea_id}
            '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
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
        query = f''' SELECT IDEAS.ID, IDEAS.NAME, IDEAS.SUMMARY FROM IDEAS{flag_reverse}{flag_amount};  '''
        self.cursor.execute(query)
        response = [res for res in self.cursor]
        return response

    def is_admin(self, check_id: int) -> bool:
        """
        Функция проверят, содержится ли id в базе админов.
        :param check_id: Проверяемый id
        :return: True, если id админский, False, если нет.
        """
        query = ''' SELECT * FROM admin_id; '''
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        return check_id in [item[0] for item in response]

    def get_language_id(self, item):
        query = f''' SELECT language_id FROM languages WHERE language_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        return 0

    def get_theme_id(self, item):
        item = item.split('-')[0]
        query = f''' SELECT id FROM themes WHERE theme_name="{item}"; '''
        self.cursor.execute(query)
        response = self.cursor.fetchone()
        if response:
            return response[0]
        return 0

    def add_suggestion(self, name='', rating=0, description='', summary='', theme='', language='', people=0, time=0,
                       level=0,
                       technologies=''):
        language = self.get_language_id(language)
        theme = self.get_theme_id(theme)
        query = """ INSERT INTO suggestions
        (NAME, RATING, DESCRIPTION, SUMMARY, theme_id, LANGUAGE_ID, PEOPLE, TIME, LEVEL, TECHNOLOGIES_ID)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?) """
        self.cursor.execute(query,
                            (name, rating, description, summary, theme, language, people, time, level, technologies))
        self.db.commit()

    def ideas_amount(self) -> int:
        """
        Метод возвращает количество идей в БД.
        :return: Число идей в БД
        """
        query = ''' SELECT COUNT(*) FROM IDEAS; '''
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

if __name__ == "__main__":
    db = BotDataBase('database.db')
    # print(db.is_admin(1234562))
    print(db.search_by_language('Python'))
    print(db.search_by_language('C#; C++'))
    # print(db.get_by_id(3))
    # db.add_suggestion('Тест 1', 11, 'Описание идеи', 'Краткое описание', 'Backend-разработка', 'Python', 3, 1)
    # db.add('Классная идея 2', 8, 'Описание идеи 2', 'Краткое описание 2',
    # 'Mobile-разработка', 'JavaScript', 3, 2)
    # db.add('Классная идея 3', 7, 'Описание идеи 3', 'Краткое описание 1',
    # 'Mobile-разработка', 'Python', 3, 3)
    # print(db.search_by_language('Python'))
    # print(db.search_by_people('более 8 человек'))
    # print(db.search_by_format('Frontend-разработка'))
    # print(db.search_by_time('срок: меньше недели'))
