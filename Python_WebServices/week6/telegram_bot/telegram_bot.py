import datetime
from collections import defaultdict

import telebot
from telebot import types

START, ADD_ADDRESS, IS_PHOTO_NEEDED, ADD_PHOTO, IS_LOCATION_NEEDED, ADD_LOCATION, END = range(7)

USER_STATE = defaultdict(lambda: START)
USER_DATA = {}

token = '616278926:AAHKgVpqO8vo1kSPyTmFE76X7h3AIE6meII'
bot = telebot.TeleBot(token)


def get_user_data(message):
    return USER_DATA.get(message.chat.id, None)


def update_user_data(message, key, value):
    id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    if id not in USER_DATA:
        USER_DATA[id] = {"current": {key: value}}
    else:
        USER_DATA[id]["current"][key] = value


def commit_user_data(message):
    id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    if id in USER_DATA:
        USER_DATA[id][str(datetime.datetime.now())] = USER_DATA[id].get('current', None)
        USER_DATA[id]['current'] = {}


def delete_user_data(message):
    id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    USER_DATA.pop(id, "Empty")


def get_state(message):
    id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    return USER_STATE[id]


def update_state(message, state):
    id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    USER_STATE[id] = state


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text="add", callback_data="add_action"),
               types.InlineKeyboardButton(text="list", callback_data="list_action"),
               types.InlineKeyboardButton(text="reset", callback_data="reset_action")]
    keyboard.add(*buttons)
    return keyboard


def create_yes_no_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text="Yes", callback_data="yes"),
               types.InlineKeyboardButton(text="No", callback_data="no")]
    keyboard.add(*buttons)
    return keyboard


# @bot.callback_query_handler(func=lambda massage: get_state(massage) == START)
# def callback_handler(callback_query):
#     message = callback_query.message
#     text_from_callback = callback_query.data
#     bot.answer_callback_query(callback_query.id, text=text_from_callback)
#     # bot.send_message(chat_id=message.chat.id, text=text_from_callback)


@bot.message_handler(commands=['start'])
def handle_message(message):
    keyboard = create_keyboard()
    bot.send_message(chat_id=message.chat.id, text="Hello my friend. Please choose what you wonna do",
                     reply_markup=keyboard)


@bot.message_handler(commands=['add'])
def handle_message(message):
    text = message.text.split("/add")
    if len(text) > 5:
        update_user_data(message, "address", text[5:])
        keyboard = create_yes_no_keyboard()
        update_state(message, IS_PHOTO_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить фото?",
                         reply_markup=keyboard)
    else:
        update_state(message, ADD_ADDRESS)
        bot.send_message(chat_id=message.chat.id, text="Введите адрессс")


@bot.message_handler(func=lambda message: get_state(message) == ADD_ADDRESS)
def handle_address_message(message):
    update_user_data(message, "address", message.text)
    keyboard = create_yes_no_keyboard()
    update_state(message, IS_PHOTO_NEEDED)
    bot.send_message(chat_id=message.chat.id, text="Хотите добавить фото?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: get_state(message) == IS_PHOTO_NEEDED)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        update_state(callback_query, ADD_PHOTO)
        bot.send_message(message.chat.id, text='Пожалуйста загрузите фото')
    else:
        update_state(callback_query, END)
        commit_user_data(message)
        bot.send_message(message.chat.id, text='Адресс был успешно добавлен')


@bot.message_handler(content_types=['photo'], func=lambda message: get_state(message) == ADD_PHOTO)
def handle_photo(message):
    file_id = message.photo[2].file_id
    update_user_data(message, "file_id", file_id)

    keyboard = create_yes_no_keyboard()
    update_state(message, IS_LOCATION_NEEDED)
    bot.send_message(chat_id=message.chat.id, text="Хотите добавить локейшен?",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: get_state(message) == IS_LOCATION_NEEDED)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        update_state(callback_query, ADD_LOCATION)
        bot.send_message(message.chat.id, text='Пожалуйста добавьте локацию')
    else:
        update_state(callback_query, END)
        commit_user_data(message)
        bot.send_message(message.chat.id, text='Адресс и фото были успешно добавлены')


@bot.message_handler(content_types=['location'], func=lambda message: get_state(message) == ADD_LOCATION)
def handle_photo(message):
    location = message.location
    update_user_data(message, "location", location)
    commit_user_data(message)
    bot.send_message(message.chat.id, text='Локация была успешно добавлена')


@bot.message_handler(commands=['list'])
def handle_message(message):
    places_list = get_user_data(message)
    if places_list:
        for place in places_list:
            if 'current' not in place:
                print(places_list[place])
                result = ''
                for key in places_list[place].keys():
                    result += "{key}: {value}\n".format(key=key, value=places_list[place][key])
                bot.send_message(chat_id=message.chat.id,
                                 text=result)
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы ничего не добавляли")


@bot.message_handler(commands=['reset'])
def handle_message_reset(message):
    delete_user_data(message)
    bot.send_message(chat_id=message.chat.id, text="Заметки были успешно удалены")


bot.polling()


