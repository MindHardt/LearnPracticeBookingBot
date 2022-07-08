import promocodes
from controller import authentificator
from database import table_admins


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if not table_admins.is_admin(user.unique_id):
        raise Exception('У вас нет прав')
    bot.send_message(message.chat.id, 'Введите число в валюте, либо 0 для админ-промокода')
    bot.register_next_step_handler(message, lambda m: handle_promocode_value(m, bot))


def handle_promocode_value(message, bot):
    value = message.text
    if value is not int:
        raise Exception('Некорректный ввод')

    code = promocodes.create_promocode(value)
    bot.send_message(message.chat.id, f'Ваш промокод: `{code}`')