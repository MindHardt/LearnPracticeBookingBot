import telebot.formatting

from controller import authentificator, config_controller


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if user is None:
        raise Exception('Вы не авторизованы!')
    if not user.is_admin:
        raise Exception('У вас нет прав')

    parts = message.text.split(' ', 2)

    config_name = parts[1]
    value = parts[2]

    old_value = config_controller.set_value(config_name, value)
    if old_value is None:
        raise Exception('Нет такой настройки!')

    bot.send_message(message.chat.id, f'Поменял значение {config_name} [{old_value} -> {value}]')