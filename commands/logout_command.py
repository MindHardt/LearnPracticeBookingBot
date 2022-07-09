from controller import authentificator


def execute(message, bot):
    user = authentificator.logout(message.chat.id)
    if user is None:
        bot.send_message(message.chat.id, 'Нельзя выйти если не вошел.')
    else:
        bot.send_message(message.chat.id, f'Успешно! До встречи, {user.name}')
