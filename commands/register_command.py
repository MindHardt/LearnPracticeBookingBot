import datetime
import hashlib
import uuid

import telebot.formatting

from controller import authentificator
from database.table_users import get_register_data


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if user is None:
        bot.send_message(message.chat.id, 'Введите как к вам обращаться, ваш логин, пароль и снова пароль с новой строки. Все значения не больше 36 символов')
        bot.register_next_step_handler(message, lambda m: handle_register_input(m, bot))
    else:
        bot.send_message(message.chat.id, 'Вы уже авторизованы!')


def handle_register_input(message, bot):
    try:
        user = get_register_data(message.text)
        user.register()
        bot.send_message(message.chat.id, f'Успешно зарегистрировал. Теперь вы можете залогиниться.')

    except Exception as e:
        errmsg = telebot.formatting.mcode(e.__str__())
        bot.send_message(message.chat.id, f'Произошла ошибка: {errmsg}')
