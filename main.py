import math

import telebot
from telebot import types
import datetime

from db import database

bot = telebot.TeleBot('6767523338:AAHCT-k6OvYwOBGzikc71QgfW75A9XxOEYM')

result_text = "Спасибо за использование нашего телеграм-бота!\n" \
              "Ниже представлены наиболее подходящие pet-проекты согласно предоставленной информации"

position = 1
def main_menu():
    global flag, suggest_position
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    language = types.KeyboardButton(text='Язык программирования')
    number = types.InlineKeyboardButton(text='Количество участников')
    markup.add(language, number)
    format = types.InlineKeyboardButton(text='Формат проекта')
    time = types.InlineKeyboardButton(text='Сроки проекта')
    markup.add(format, time)
    list_all = types.InlineKeyboardButton(text='Показать все pet-проекты')
    suggest_idea = types.InlineKeyboardButton(text='Предложить идею')
    markup.add(list_all, suggest_idea)
    admin_enter = types.InlineKeyboardButton(text='Войти от имени модератора')
    markup.add(admin_enter)
    flag = 0
    suggest_position = 0
    suggest_list.clear()
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


def format_day(num):
    if num == 1:
        return f"{num} день"
    elif num in (2, 3, 4):
        return f"{num} дня"
    else:
        return f"{num} дней"


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

def confirmation():
    conf = types.InlineKeyboardMarkup()
    confT = types.InlineKeyboardButton(text="Отправить идею", callback_data='confirmation_true' + str(data[0]))
    conf.row(confT)
    confF = types.InlineKeyboardButton(text="Пересоздать заново", callback_data='confirmation_false' + str(data[0]))
    conf.row(confF)
    return conf

def database_language(message):
    message = message.replace(' ', '|', 1)
    db = database.BotDataBase('db/database.db')
    answer = db.search_by_language(message.split('|')[1].split('; '))
    return answer


def database_number(message):
    db = database.BotDataBase('db/database.db')
    answer = db.search_by_people(message)
    return answer


def database_format(message):
    db = database.BotDataBase('db/database.db')
    answer = db.search_by_format(message[13:])
    return answer


def database_time(message):
    db = database.BotDataBase('db/database.db')
    answer = db.search_by_time(message)
    return answer

def database_all():
    db = database.BotDataBase('db/database.db')
    answer = db.get_all()
    return answer
def murkup_all():
    list = database_all()
    db = types.InlineKeyboardMarkup()
    for i in range ((position-1)*5,position*5):
        if i<len(list):
            project = types.InlineKeyboardButton(text=list[i][1] + " - " + list[i][2], callback_data='project_' + str(list[i][0]))
            db.row(project)
    left = types.InlineKeyboardButton(text='<', callback_data='left_message')
    pos = types.InlineKeyboardButton(text=str(position) + '/'+ str(math.ceil(len(list)/5)), callback_data='pos_message')
    right = types.InlineKeyboardButton(text='>', callback_data='right_message')
    db.row(left, pos, right)
    back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
    db.row(back)
    return db
def get_time():
    all_time = str(datetime.datetime.now())
    years = all_time[0:4]
    month = all_time[5:7]
    day = all_time[8:10]
    time = all_time[10:19]
    return "Все pet-проекты загруженные до" + time + " " + day + "." + month + "." + years

@bot.message_handler(commands=['start'])
def start(message):
    first_mess = f"{message.from_user.first_name} {message.from_user.last_name}, здраствуйте,\n" \
                 f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                 f"Прежде чем начать, пожалуйста, выберите категорию поиска"
    bot.send_message(message.chat.id, first_mess, reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: True)
def call_query(call):
    global position
    if call.message:
        if call.data[0:7] == 'project':
            info_db = database.BotDataBase('db/database.db')
            data = info_db.get_by_id(int(call.data.split('_')[1]))
            string = "Название проекта: " + str(data[1]) + "\n" + \
                     "Рейтинг: " + str(data[2]) + "\n" + \
                     "Описание: " + str(data[3]) + "\n" + \
                     "Направление: " + str(data[5]) + "\n" + \
                     "Количество участников: " + str(data[7]) + "\n" + \
                     "Сроки реализации: " + format_day(data[8]) + "\n" + \
                     "Язык программирования: " + str(data[6]) + "\n" + \
                     "Сложность: " + str(data[9]) + '/10' + "\n" + \
                     "Предлагаемые технологии: " + str(data[11]) + "\n"
            db = types.InlineKeyboardMarkup()
            back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
            db.row(back)
            bot.send_message(call.message.chat.id, string, reply_markup=db)
        if call.data == 'right_message':
            db = database.BotDataBase('db/database.db')
            if db.ideas_amount() > position*5:
                position = position + 1
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, get_time(), reply_markup=murkup_all())
        if call.data == 'left_message':
            if position > 1:
                position = position - 1
                bot.delete_message(call.message.chat.id, call.message.id)
                bot.send_message(call.message.chat.id, get_time(), reply_markup=murkup_all())
        if call.data == 'confirmation_true':
            bot.send_message(call.message.chat.id, "Идея отправлена модератору (на самом деле ещё нет)")
            print("true")
        if call.data == 'confirmation_false':
            global flag, suggest_position
            flag = 1
            suggest_position = 0
            suggest_list.clear()
            bot.send_message(call.message.chat.id, "Введите название вашей идеи")
        if call.data == 'back_message':
            first_mess = f"{call.from_user.first_name} {call.from_user.last_name}, здраствуйте,\n" \
                         f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                         f"Прежде чем начать, пожалуйста, выберите категорию поиска"
            position = 1
            bot.send_message(call.message.chat.id, first_mess, reply_markup=main_menu())

flag = 0
suggest_position = 0
suggest_list = []
@bot.message_handler(content_types=['text'])
def marshrutisator(message):
    if flag == 0:
        call_message(message)
    else:
        suggest_message(message)
def call_message(message):
    if message.text == 'Язык программирования':
        bot.send_message(message.chat.id, "Выбирете подходящий язык реализации проекта", reply_markup=language_func())
    elif message.text == 'Количество участников':
        bot.send_message(message.chat.id, "Выбирете количество участников проекта", reply_markup=number_func())
    elif message.text == 'Формат проекта':
        bot.send_message(message.chat.id, "Выбирете подходящий формат разработки", reply_markup=format_func())
    elif message.text == 'Сроки проекта':
        bot.send_message(message.chat.id, "Выбирете подходящие вам сроки проекта", reply_markup=time_func())
    elif message.text == 'Показать все pet-проекты':
        bot.send_message(message.chat.id, text=get_time(), parse_mode='Markdown', reply_markup=murkup_all())
    elif str(message.text)[0:4] == 'язык':
        # bot.send_message(message.chat.id, result_text + "\n" + database_language(message.text), parse_mode= 'Markdown', reply_markup=db_language_func())
        bot.send_message(message.chat.id, result_text)
        list = database_language(message.text)
        for data in list:
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=data[1], callback_data='project_' + str(data[0]))
            db.row(project)
            bot.send_message(message.chat.id, data[1] + "\n" + data[2], parse_mode='Markdown', reply_markup=db)
        if not list:
            bot.send_message(message.chat.id, "Не найдено ни одного pet-проекта. Попробуйте изменить параметры посика.")
        db_language = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_language.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_language)
    elif (str(message.text)[len(str(message.text)) - 7:len(str(message.text))] == 'человек') | (
            str(message.text)[len(str(message.text)) - 8:len(str(message.text))] == 'человека'):
        bot.send_message(message.chat.id, result_text)
        list = database_number(message.text)
        for data in list:
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=data[1], callback_data='project_' + str(data[0]))
            db.row(project)
            bot.send_message(message.chat.id, data[1] + "\n" + data[2], parse_mode='Markdown', reply_markup=db)
        if not list:
            bot.send_message(message.chat.id, "Не найдено ни одного pet-проекта. Попробуйте изменить параметры посика.")
        db_number = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_number.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_number)
    elif str(message.text)[0:11] == 'направление':
        bot.send_message(message.chat.id, result_text)
        list = database_format(message.text)
        for data in list:
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=data[1], callback_data='project_' + str(data[0]))
            db.row(project)
            bot.send_message(message.chat.id, data[1] + "\n" + data[2], parse_mode='Markdown', reply_markup=db)
        if not list:
            bot.send_message(message.chat.id, "Не найдено ни одного pet-проекта. Попробуйте изменить параметры посика.")
        db_format = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_format.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_format)
    elif str(message.text)[0:4] == 'срок':
        bot.send_message(message.chat.id, result_text)
        list = database_time(message.text)
        for data in list:
            db = types.InlineKeyboardMarkup()
            project = types.InlineKeyboardButton(text=data[1], callback_data='project_' + str(data[0]))
            db.row(project)
            bot.send_message(message.chat.id, data[1] + "\n" + data[2], parse_mode='Markdown', reply_markup=db)
        if not list:
            bot.send_message(message.chat.id, "Не найдено ни одного pet-проекта. Попробуйте изменить параметры посика.")
        db_time = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text='В главное меню', callback_data='back_message')
        db_time.row(back)
        bot.send_message(message.chat.id, text="Или вернитесь в главное меню", reply_markup=db_time)
    elif message.text == 'Предложить идею':
        bot.send_message(message.chat.id, "Введите название вашей идеи")
        global flag
        flag = 1
    elif message.text == 'Назад':
        first_mess = f"{message.from_user.first_name} {message.from_user.last_name}, здраствуйте,\n" \
                     f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                     f"Прежде чем начать, пожалуйста, выберите категорию поиска"
        bot.send_message(message.chat.id, first_mess, reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "раздел в разработке")
def suggest_message(message):
    global suggest_position
    if suggest_position == 0:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите краткое описание")
        suggest_position = suggest_position + 1
    elif suggest_position == 1:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите полное описание")
        suggest_position = suggest_position + 1
    elif suggest_position == 2:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите подходящий язык реализации проекта", reply_markup=language_func())
        suggest_position = suggest_position + 1
    elif suggest_position == 3:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите количество участников проекта", reply_markup=number_func())
        suggest_position = suggest_position + 1
    elif suggest_position == 4:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите подходящий формат разработки", reply_markup=format_func())
        suggest_position = suggest_position + 1
    elif suggest_position == 5:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите срок реализации проекта", reply_markup=time_func())
        suggest_position = suggest_position + 1
    elif suggest_position == 6:
        suggest_list.append(message.text)
        bot.send_message(message.chat.id, "Введите предлагаемые технологии")
        suggest_position = suggest_position + 1
    elif suggest_position == 7:
        suggest_list.append(message.text)
        conf = types.InlineKeyboardMarkup()
        confT = types.InlineKeyboardButton(text="Отправить идею", callback_data='confirmation_true')
        conf.row(confT)
        confF = types.InlineKeyboardButton(text="Пересоздать заново", callback_data='confirmation_false')
        conf.row(confF)
        confBack = types.InlineKeyboardButton(text="Вернуться в главное меню", callback_data='back_message')
        conf.row(confBack)
        bot.send_message(message.chat.id, "Проверьте введённую информацию\n" +
                         "Название идеи: " + suggest_list[0] + "\n" +
                         "Краткое описание: " + suggest_list[1] + "\n" +
                         "Полное описание: " + suggest_list[2] + "\n" +
                         suggest_list[3] + "\n" +
                         "Количество участников: " + suggest_list[4] + "\n" +
                         suggest_list[5] + "\n" +
                         suggest_list[6] + "\n" +
                         "Предлагаемые технологии: " + suggest_list[7], reply_markup=conf)
        suggest_position = suggest_position + 1
# bot.delete_message(message.chat.id, message.message_id)
# bot.answer_callback_query(callback_query_id=message.id, show_alert=False)


bot.polling()
