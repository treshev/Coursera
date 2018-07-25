import datetime
import json
from collections import defaultdict

import redis
import telebot
from telebot import types

START, ADD_ADDRESS, IS_PHOTO_NEEDED, ADD_PHOTO, IS_LOCATION_NEEDED, ADD_LOCATION, END = range(7)

USER_STATE = defaultdict(lambda: START)
USER_DATA = {}

token = '616278926:AAHKgVpqO8vo1kSPyTmFE76X7h3AIE6meII'
bot = telebot.TeleBot(token)

IS_REDIS = True
redis_connection = None


def get_redis_connection():
    global redis_connection
    if redis_connection is None:
        redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)
    return redis_connection


def get_user_data(user_id):
    if IS_REDIS:
        r = get_redis_connection()
        user_binary_data = r.get(user_id)
        user_data = json.loads(user_binary_data) if user_binary_data else None
        return user_data
    else:
        return USER_DATA.get(user_id, None)


def update_user_data(user_id, key, value):
    if IS_REDIS:
        r = get_redis_connection()
        user = r.get(user_id)
        if not user:
            user_data = {"current": {key: value}}
        else:
            user_data = json.loads(user)
            if isinstance(user_data['current'], str):
                user_data["current"] = {key: value}
            else:
                user_data["current"][key] = value
        print(user_data)
        r.set(user_id, json.dumps(user_data))
    else:
        if user_id not in USER_DATA:
            USER_DATA[user_id] = {"current": {key: value}}
        else:
            USER_DATA[user_id]["current"][key] = value


def commit_user_data(user_id):
    if IS_REDIS:
        r = get_redis_connection()
        user = r.get(user_id)
        if user:
            user_data = json.loads(user)
            user_data[str(datetime.datetime.now())] = user_data.get('current', None)
            user_data['current'] = ''
            r.set(user_id, json.dumps(user_data))
    else:
        if user_id in USER_DATA:
            USER_DATA[user_id][str(datetime.datetime.now())] = USER_DATA[user_id].get('current', None)
            USER_DATA[user_id]['current'] = {}


def delete_user_data(user_id):
    if IS_REDIS:
        r = get_redis_connection()
        r.delete(user_id)
    else:
        USER_DATA.pop(user_id, "Empty")


def get_state(user_id):
    if IS_REDIS:
        r = get_redis_connection()
        user_state_data = r.get("USER_STATE_{}".format(user_id))
        user_data = int(user_state_data) if user_state_data else None
        return user_data
    else:
        return USER_STATE[user_id]


def update_state(message, state):
    user_id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    if IS_REDIS:
        r = get_redis_connection()
        r.set("USER_STATE_{}".format(user_id), state)
    else:
        USER_STATE[user_id] = state


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


@bot.message_handler(commands=['start'])
def handle_start_message(message):
    keyboard = create_keyboard()
    bot.send_message(chat_id=message.chat.id, text="Hello my friend. Please choose what you wonna do",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda
        callback_query: callback_query.data == 'add_action' or callback_query.data == 'list_action' or callback_query.data == 'reset_action')
def handle_initial_commands(callback_query):
    if callback_query.data == 'add_action':
        handle_add_command(callback_query.message)
    elif callback_query.data == 'list_action':
        handle_list_command(callback_query.message)
    elif callback_query.data == 'reset_action':
        handle_reset_command(callback_query.message)


@bot.message_handler(commands=['add'])
def handle_add_command(message):
    text = message.text.split(" ")
    user_id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    if "add" in message.text and len(text) > 1:
        update_user_data(user_id, "address", text[5:])
        keyboard = create_yes_no_keyboard()
        update_state(message, IS_PHOTO_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить фото?",
                         reply_markup=keyboard)
    else:
        update_state(message, ADD_ADDRESS)
        bot.send_message(chat_id=user_id, text="Введите адрес")


@bot.callback_query_handler(func=lambda message: get_state(message.message.chat.id) == IS_PHOTO_NEEDED)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        update_state(callback_query, ADD_PHOTO)
        bot.send_message(message.chat.id, text='Пожалуйста загрузите фото')
    else:
        keyboard = create_yes_no_keyboard()
        update_state(message, IS_LOCATION_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить локейшен?",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: get_state(message.message.chat.id) == IS_LOCATION_NEEDED)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        update_state(callback_query, ADD_LOCATION)
        bot.send_message(message.chat.id, text='Пожалуйста добавьте локацию')
    else:
        update_state(callback_query, END)
        commit_user_data(message.chat.id)
        bot.send_message(message.chat.id, text='Адресс был успешно добавлен')


@bot.message_handler(func=lambda message: get_state(message.chat.id) == ADD_ADDRESS)
def handle_address_message(message):
    user_id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    if message.text and "list" not in message.text and "reset" not in message.text:
        update_user_data(user_id, "address", message.text)
        keyboard = create_yes_no_keyboard()
        update_state(message, IS_PHOTO_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить фото?",
                         reply_markup=keyboard)
    else:
        update_state(user_id, START)


@bot.message_handler(content_types=['photo'], func=lambda message: get_state(message.chat.id) == ADD_PHOTO)
def handle_photo(message):
    file_id = message.photo[-1].file_id
    update_user_data(message.chat.id, "file_id", file_id)

    keyboard = create_yes_no_keyboard()
    update_state(message, IS_LOCATION_NEEDED)
    bot.send_message(chat_id=message.chat.id, text="Хотите добавить локейшен?",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['location'], func=lambda message: get_state(message.chat.id) != ADD_LOCATION)
def handle_photo(message):
    bot.send_message(message.chat.id, text='Объект был успешно добавлен')


@bot.message_handler(content_types=['location'], func=lambda message: get_state(message.chat.id) == ADD_LOCATION)
def handle_photo(message):
    location = message.location
    update_user_data(message.chat.id, "location", [location.latitude, location.longitude])
    commit_user_data(message.chat.id)
    bot.send_message(message.chat.id, text='Объект был успешно добавлен')


@bot.message_handler(commands=['list'])
def handle_list_command(message):
    user_id = message.message.chat.id if isinstance(message, types.CallbackQuery) else message.chat.id
    places_list = get_user_data(user_id)
    if places_list:
        i = 1
        for place in places_list:
            if 'current' not in place:
                item = places_list[place]
                title_text = "<b>{}</b>. {}".format(i, item["address"])
                bot.send_message(chat_id=message.chat.id, text=title_text, parse_mode="HTML")

                if "file_id" in item.keys():
                    bot.send_photo(chat_id=message.chat.id, photo=item["file_id"])

                if "location" in item.keys():
                    location = item["location"]
                    bot.send_location(message.chat.id, location[0], location[1])
                if i < 10:
                    i += 1
                else:
                    return

    else:
        bot.send_message(chat_id=message.chat.id,
                         text="У вас нет добавленных объектов")


@bot.message_handler(commands=['reset'])
def handle_reset_command(message):
    delete_user_data(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Заметки были успешно удалены")


bot.polling()
