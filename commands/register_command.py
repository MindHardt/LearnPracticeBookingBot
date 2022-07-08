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
        bot.send_message(message.chat.id, 'Введите как к вам обращаться, ваш логин, пароль и снова пароль с новой строки. Все значения не больше 36 символов')
        bot.register_next_step_handler(message, lambda m: handle_register_input(m, bot))


def handle_register_input(message, bot):
    try:
        values = message.text.split('\n', 4)
        for value in values:
            if len(value) > 36 or len(value) == 0:
                raise Exception('Некорректные данные')

        name = values[0]
        login = values[1]
        pass1 = values[2]
        pass2 = values[3]

        if pass1 != pass2:
            raise Exception('Пароли не совпадают')

        user = EntityUser()
        user.name = name
        user.login = login
        user.balance = 0
        user.unique_id = uuid.uuid4().__str__()
        user.password_hash = hashlib.sha224(pass1.encode()).hexdigest()

        table_users.try_register(user)
        bot.send_message(message.chat.id, f'Успешно зарегистрировал. Теперь вы можете залогиниться.')

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')
