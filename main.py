import telebot
from telebot import types

bot = telebot.TeleBot('')

def main_menu():
    markup = types.InlineKeyboardMarkup()
    language = types.InlineKeyboardButton(text='Язык программирования', callback_data='language_message')
    number = types.InlineKeyboardButton(text='Количество участников', callback_data='number_message')
    markup.row(language, number)
    format = types.InlineKeyboardButton(text='Формат проекта', callback_data='format_message')
    time = types.InlineKeyboardButton(text='Сроки проекта', callback_data='time_message')
    markup.row(format, time)
    return markup

def language_func():
    language = types.InlineKeyboardMarkup()
    si = types.InlineKeyboardButton(text='C; C++; C#', callback_data='si_message')
    python = types.InlineKeyboardButton(text='Python', callback_data='python_message')
    language.row(si, python)
    html = types.InlineKeyboardButton(text='HTML; MySQL', callback_data='html_message')
    java = types.InlineKeyboardButton(text='JavaScript', callback_data='java_message')
    language.row(html, java)
    back = types.InlineKeyboardButton(text='Назад', callback_data='back_message')
    language.row(back)
    return language

def number_func():
    number = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton(text='1', callback_data='one_message')
    two = types.InlineKeyboardButton(text='2', callback_data='two_message')
    number.row(one, two)
    five = types.InlineKeyboardButton(text='3-8', callback_data='five_message')
    nine = types.InlineKeyboardButton(text='более 8', callback_data='nine_message')
    number.row(five, nine)
    back = types.InlineKeyboardButton(text='Назад', callback_data='back_message')
    number.row(back)
    return number

def format_func():
    format = types.InlineKeyboardMarkup()
    backend = types.InlineKeyboardButton(text='Backend-разработка', callback_data='backend_message')
    frontend = types.InlineKeyboardButton(text='Frontend-разработка', callback_data='frontend_message')
    format.row(backend, frontend)
    mobile = types.InlineKeyboardButton(text='Mobile-разработка', callback_data='mobile_message')
    back = types.InlineKeyboardButton(text='Назад', callback_data='back_message')
    format.row(mobile, back)
    return format

def time_func():
    time = types.InlineKeyboardMarkup()
    week = types.InlineKeyboardButton(text='неделя', callback_data='week_message')
    mouth = types.InlineKeyboardButton(text='месяц', callback_data='mouth_message')
    time.row(week, mouth)
    six_mouth = types.InlineKeyboardButton(text='полгода', callback_data='six_mouth_message')
    twelve_mouth = types.InlineKeyboardButton(text='более полугода', callback_data='twelve_mouth_message')
    time.row(six_mouth, twelve_mouth)
    back = types.InlineKeyboardButton(text='Назад', callback_data='back_message')
    time.row(back)
    return time

@bot.message_handler(commands=['start'])
def start(message):
    first_mess = f"{message.from_user.first_name} {message.from_user.last_name}, здраствуйте,\n" \
                 f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                 f"Прежде чем начать, пожалуйста, выберите категорию поиска"
    bot.send_message(message.chat.id, first_mess, reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def call_query(call):
    if call.message:
        if call.data == 'language_message':
            bot.send_message(call.message.chat.id, "Выбирете подходящий язык реализации проекта", reply_markup=language_func())
        elif call.data == 'number_message':
            bot.send_message(call.message.chat.id, "Выбирете количество участников проекта", reply_markup=number_func())
        elif call.data == 'format_message':
            bot.send_message(call.message.chat.id, "Выбирете подходящий формат разработки", reply_markup=format_func())
        elif call.data == 'time_message':
            bot.send_message(call.message.chat.id, "Выбирете подходящие вам сроки проекта", reply_markup=time_func())
        elif call.data == 'back_message':
            first_mess = f"{call.from_user.first_name} {call.from_user.last_name}, здраствуйте,\n" \
                         f"В нашем телеграм-боте вы сможете найти подходящие вам идеи pet-проектов. Вне зависимости от вашего уровня программирования, вы точно не уйдёте с пустыми руками\n" \
                         f"Прежде чем начать, пожалуйста, выберите категорию поиска"
            bot.send_message(call.message.chat.id, first_mess, reply_markup=main_menu())
        else:
            bot.send_message(call.message.chat.id, "раздел в разработке")
    bot.answer_callback_query(callback_query_id=call.id, show_alert=False)

bot.polling()
