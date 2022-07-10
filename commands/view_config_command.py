from controller import authentificator
from controller.config_controller import get_config


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if user is None:
        raise Exception('Вы не авторизованы!')
    if not user.is_admin:
        raise Exception('У вас нет прав')

    config = get_config()

    bot.send_message(message.chat.id, config)
