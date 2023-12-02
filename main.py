import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('')

result_text = "Спасибо за использование нашего телеграм-бота!\n" \
    "Ниже представлены наиболее подходящие pet-проекты согласно предоставленной информации"
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    language = types.KeyboardButton(text='Язык программирования')
    number = types.InlineKeyboardButton(text='Количество участников')
    markup.add(language, number)
    format = types.InlineKeyboardButton(text='Формат проекта')
    time = types.InlineKeyboardButton(text='Сроки проекта')
    markup.add(format, time)
    return markup

def language_func():
    language = types.ReplyKeyboardMarkup(resize_keyboard=True)
    si = types.KeyboardButton(text='языки: C; C++; C#')
    python = types.KeyboardButton(text='язык: Python')
    language.add(si, python)
    html = types.KeyboardButton(text='языки: HTML; MySQL')
    java = types.KeyboardButton(text='язык: JavaScript')
    language.add(html, java)
    back = types.KeyboardButton(text='Назад')
    language.add(back)
    return language

def number_func():
    number = types.ReplyKeyboardMarkup()
    one = types.KeyboardButton(text='1 человек')
    two = types.KeyboardButton(text='2 человека')
    number.row(one, two)
    five = types.KeyboardButton(text='3-8 человек')
    nine = types.KeyboardButton(text='более 8 человек')
    number.row(five, nine)
    back = types.KeyboardButton(text='Назад')
    number.row(back)
    return number

def format_func():
    format = types.ReplyKeyboardMarkup()
    backend = types.KeyboardButton(text='направление: Backend-разработка')
    frontend = types.KeyboardButton(text='направление: Frontend-разработка')
    format.row(backend, frontend)
    mobile = types.KeyboardButton(text='направление: Mobile-разработка')
    back = types.KeyboardButton(text='Назад')
    format.row(mobile, back)
    return format

def time_func():
    time = types.ReplyKeyboardMarkup()
    week = types.KeyboardButton(text='срок: меньше недели')
    mouth = types.KeyboardButton(text='срок: от недели до месяца')
    time.row(week, mouth)
    six_mouth = types.KeyboardButton(text='срок: от месяца до полугода')
    twelve_mouth = types.KeyboardButton(text='срок: более полугода')
    time.row(six_mouth, twelve_mouth)
    back = types.KeyboardButton(text='Назад')
    time.row(back)
    return time

def database_language(message):
    sqlite_connection = sqlite3.connect('dbtest.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = """SELECT * from idea"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    list = []
    for row in records:
        if str(row[7])[len(str(row[7]))-6:len(str(row[7]))] == str(message)[len(str(message))-6:len(str(message))]:
            list.append(row[0])
            list.append(row[3])
    return list
def database_number(message):
    sqlite_connection = sqlite3.connect('dbtest.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = """SELECT * from idea"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    list = []
    for row in records:
        k = False
        if message == "1 человек":
            k = (row[5] == 1)
        elif message == "2 человека":
            k = (row[5] == 2)
        elif message == "3-8 человек":
            k = (row[5] >= 3 & row[5] <= 8)
        elif message == "более 8 человек":
            k = (row[5] > 8)
        if k:
            list.append(row[0])
            list.append(row[3])
    return list

def database_format(message):
    sqlite_connection = sqlite3.connect('dbtest.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = """SELECT * from idea"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    list = []
    for row in records:
        if str(row[4])[len(str(row[4])) - 17:len(str(row[4]))] == str(message)[len(str(message)) - 17:len(str(message))]:
            list.append(row[0])
            list.append(row[3])
    return list

def database_time(message):
    sqlite_connection = sqlite3.connect('dbtest.db')
    cursor = sqlite_connection.cursor()
    sqlite_select_query = """SELECT * from idea"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    list = []
    for row in records:
        value = int(str(row[6])[0:str(row[6]).find(" ")])
        k = False
        if message == "срок: меньше недели":
            k = (value < 7)
        elif message == "срок: от недели до месяца":
            k = (value >= 7) & (value <= 31)
        elif message == "срок: от месяца до полугода":
            k = ((value > 31) & (value <= 180))
        elif message == "срок: более полугода":
            k = (value > 180)
        if k:
            list.append(row[0])
            list.append(row[3])
    return list

@bot.message_handler(commands=['start'])
def start(message):
    first_mess = f"{message.from_user.first_name} {message.from_user.last_name}, здраствуйте,\n" \
                 f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                 f"Прежде чем начать, пожалуйста, выберите категорию поиска"
    bot.send_message(message.chat.id, first_mess, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def call_query(call):
    if call.message:
        if call.data == 'back_message':
            first_mess = f"{call.from_user.first_name} {call.from_user.last_name}, здраствуйте,\n" \
                         f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                         f"Прежде чем начать, пожалуйста, выберите категорию поиска"
            bot.send_message(call.message.chat.id, first_mess, reply_markup=main_menu())

@bot.message_handler(content_types=['text'])
def call_message(message):
    if message.text == 'Язык программирования':
        bot.send_message(message.chat.id, "Выбирете подходящий язык реализации проекта", reply_markup=language_func())
    elif message.text == 'Количество участников':
        bot.send_message(message.chat.id, "Выбирете количество участников проекта", reply_markup=number_func())
    elif message.text == 'Формат проекта':
        bot.send_message(message.chat.id, "Выбирете подходящий формат разработки", reply_markup=format_func())
    elif message.text == 'Сроки проекта':
        bot.send_message(message.chat.id, "Выбирете подходящие вам сроки проекта", reply_markup=time_func())
    elif str(message.text)[0:4] == 'язык':
        #bot.send_message(message.chat.id, result_text + "\n" + database_language(message.text), parse_mode= 'Markdown', reply_markup=db_language_func())
        bot.send_message(message.chat.id, result_text)
        list = database_language(message.text)
        i = 0
        while i<len(list):
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=list[i], callback_data='project_n')
            db.row(project)
            bot.send_message(message.chat.id, list[i] + "\n" + list[i+1], parse_mode='Markdown', reply_markup=db)
            i = i + 2
        db_language = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_language.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_language)
    elif (str(message.text)[len(str(message.text))-7:len(str(message.text))] == 'человек') | (str(message.text)[len(str(message.text))-8:len(str(message.text))] == 'человека'):
        bot.send_message(message.chat.id, result_text)
        list = database_number(message.text)
        i = 0
        while i < len(list):
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=list[i], callback_data='project_n')
            db.row(project)
            bot.send_message(message.chat.id, list[i] + "\n" + list[i + 1], parse_mode='Markdown', reply_markup=db)
            i = i + 2
        db_number = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_number.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_number)
    elif str(message.text)[0:11] == 'направление':
        bot.send_message(message.chat.id, result_text)
        list = database_format(message.text)
        i = 0
        while i < len(list):
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=list[i], callback_data='project_n')
            db.row(project)
            bot.send_message(message.chat.id, list[i] + "\n" + list[i + 1], parse_mode='Markdown', reply_markup=db)
            i = i + 2
        db_format = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_format.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_format)
    elif str(message.text)[0:4] == 'срок':
        bot.send_message(message.chat.id, result_text)
        list = database_time(message.text)
        i = 0
        while i < len(list):
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=list[i], callback_data='project_n')
            db.row(project)
            bot.send_message(message.chat.id, list[i] + "\n" + list[i + 1], parse_mode='Markdown', reply_markup=db)
            i = i + 2
        db_time = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_time.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_time)
    elif message.text == 'Назад':
        first_mess = f"{message.from_user.first_name} {message  .from_user.last_name}, здраствуйте,\n" \
                         f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                         f"Прежде чем начать, пожалуйста, выберите категорию поиска"
        bot.send_message(message.chat.id, first_mess, reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "раздел в разработке")
    #bot.delete_message(call.message.chat.id, call.message.message_id)
    #bot.answer_callback_query(callback_query_id=message.id, show_alert=False)

bot.polling()
