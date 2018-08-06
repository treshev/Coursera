import logging
import os

import telebot
from flask import Flask, request
from telebot import types

import connector

START, ADD_ADDRESS, IS_PHOTO_NEEDED, ADD_PHOTO, IS_LOCATION_NEEDED, ADD_LOCATION, END = range(7)

token = '616278926:AAHKgVpqO8vo1kSPyTmFE76X7h3AIE6meII'
bot = telebot.TeleBot(token)

IS_REDIS = True
connection = connector.RedisConnector()


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
    bot.send_message(chat_id=message.chat.id,
                     text="Приветствую Вас. \nВы можете добавить объект использую команду\n/add <b>адрес объекта</b>\n или использовать одну из кнопок ниже",
                     reply_markup=keyboard, parse_mode="HTML")


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
    if "add" in message.text and len(text) > 1:
        keyboard = create_yes_no_keyboard()
        connection.update_user_data(message.chat.id, "address", message.text[5:])
        connection.update_state(message.chat.id, IS_PHOTO_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить фото?",
                         reply_markup=keyboard)
    else:
        connection.update_state(message.chat.id, ADD_ADDRESS)
        bot.send_message(chat_id=message.chat.id, text="Введите адрес")


@bot.callback_query_handler(func=lambda message: connection.get_state(message.message.chat.id) == IS_PHOTO_NEEDED)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        connection.update_state(message.chat.id, ADD_PHOTO)
        bot.send_message(message.chat.id, text='Пожалуйста загрузите фото')
    else:
        keyboard = create_yes_no_keyboard()
        connection.update_state(message.chat.id, IS_LOCATION_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить локейшен?",
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda message: connection.get_state(message.message.chat.id) == IS_LOCATION_NEEDED)
def callback_handler(callback_query):
    data = callback_query.data
    message = callback_query.message
    if data == 'yes':
        connection.update_state(message.chat.id, ADD_LOCATION)
        bot.send_message(message.chat.id, text='Пожалуйста добавьте локацию')
    else:
        connection.update_state(message.chat.id, END)
        connection.commit_user_data(message.chat.id)
        bot.send_message(message.chat.id, text='Адресс был успешно добавлен')


@bot.message_handler(func=lambda message: connection.get_state(message.chat.id) == ADD_ADDRESS)
def handle_address_message(message):
    if message.text and "list" not in message.text and "reset" not in message.text:
        connection.update_user_data(message.chat.id, "address", message.text)
        keyboard = create_yes_no_keyboard()
        connection.update_state(message.chat.id, IS_PHOTO_NEEDED)
        bot.send_message(chat_id=message.chat.id, text="Хотите добавить фото?",
                         reply_markup=keyboard)
    else:
        connection.update_state(message.chat.id, START)


@bot.message_handler(content_types=['photo'], func=lambda message: connection.get_state(message.chat.id) == ADD_PHOTO)
def handle_photo(message):
    file_id = message.photo[-1].file_id
    connection.update_user_data(message.chat.id, "file_id", file_id)

    keyboard = create_yes_no_keyboard()
    connection.update_state(message.chat.id, IS_LOCATION_NEEDED)
    bot.send_message(chat_id=message.chat.id, text="Хотите добавить локейшен?",
                     reply_markup=keyboard)


# @bot.message_handler(content_types=['location'],
#                      func=lambda message: connection.get_state(message.chat.id) != ADD_LOCATION)
# def handle_photo(message):
#     bot.send_message(message.chat.id, text='Объект был успешно добавлен')


@bot.message_handler(content_types=['location'],
                     func=lambda message: connection.get_state(message.chat.id) == ADD_LOCATION)
def handle_photo(message):
    location = message.location
    connection.update_user_data(message.chat.id, "location", [location.latitude, location.longitude])
    connection.commit_user_data(message.chat.id)
    bot.send_message(message.chat.id, text='Объект был успешно добавлен')


@bot.message_handler(commands=['list'])
def handle_list_command(message):
    places_list = connection.get_user_data(message.chat.id)
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
    connection.delete_user_data(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Заметки были успешно удалены")


if __name__ == '__main__':
    if "HEROKU" in list(os.environ.keys()):

        logger = telebot.logger
        telebot.logger.setLevel(logging.INFO)
        server = Flask(__name__)


        @server.route("/bot", methods=['POST'])
        def getMessage():
            bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
            return "!", 200


        @server.route("/")
        def webhook():
            bot.remove_webhook()
            bot.set_webhook(
                url="https://curserabot.herokuapp.com/bot")  # этот url нужно заменить на url вашего Хероку приложения
            return "?", 200


        server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
    else:
        # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
        # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
        bot.remove_webhook()
        bot.polling(none_stop=True)
