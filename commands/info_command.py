import telebot.formatting

from controller import authentificator


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if user is None:
        bot.send_message(message.chat.id, 'Вы не авторизованы!')
    else:
        infotab = str()
        infotab += f'Ваш айди: {user.unique_id}\n'
        infotab += f'Ваше имя: {user.name}\n'
        infotab += f'Ваш баланс: {user.balance}\n'
        bot.send_message(message.chat.id, infotab)


def handle_login_input(message, bot):
    try:
        values = message.text.split('\n', 1)
        for value in values:
            if len(value) > 36 or len(value) == 0:
                raise Exception('Некорректные данные')

        login = values[0]
        password = values[1]
        # print(f'Trying to fetch user with login {login} and password_hash {password}')
        user = table_users.auth(login, password)
        authentificator.auth(user, message.chat.id)
        bot.send_message(message.chat.id, f'Успешно! Приветствую, {user.name}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')