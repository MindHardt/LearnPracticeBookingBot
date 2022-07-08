import uuid

from controller import authentificator
from database import table_users
from database.entity_user import EntityUser


def execute(message, bot):
    try:
        user = authentificator.get_user(message.chat.id)
        bot.send_message(message.chat.id, 'Вы уже авторизованы!')
    except KeyError:
        bot.send_message(message.chat.id, 'Введите логин и пароль, каждый на новой строке')
        bot.register_next_step(message.chat.id, lambda m: handle_login_input(m, bot))


def handle_login_input(message, bot):
    values = message.text.split('\n', 1)
    for value in values:
        if value.len > 36 or value.len == 0:
            raise Exception('Некорректные данные')

    login = values[0]
    password_hash = values[1].__hash__()

    user = table_users.auth(login, password_hash)
