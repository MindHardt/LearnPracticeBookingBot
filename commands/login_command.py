import hashlib
import uuid

from controller import authentificator
from database import table_users
from database.entity_user import EntityUser


def execute(message, bot):
    try:
        authentificator.get_user(message.chat.id)
        bot.send_message(message.chat.id, 'Вы уже авторизованы!')
    except KeyError:
        bot.send_message(message.chat.id, 'Введите логин и пароль, каждый на новой строке')
        bot.register_next_step_handler(message, lambda m: handle_login_input(m, bot))


def handle_login_input(message, bot):
    try:
        values = message.text.split('\n', 1)
        for value in values:
            if len(value) > 36 or len(value) == 0:
                raise Exception('Некорректные данные')

        login = values[0]
        password = values[1]
        password_hash = hashlib.sha224(password.encode()).hexdigest()
        print(f'Trying to fetch user with login {login} and password_hash {password_hash}')
        user = table_users.auth(login, password_hash)
        authentificator.login(user, message.chat.id)
        bot.send_message(message.chat.id, f'Успешно! Приветствую, {user.name}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')
