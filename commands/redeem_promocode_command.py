import promocodes
from controller import authentificator
from database.entity_user import EntityUser


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    bot.send_message(message.chat.id, 'Введите промокод')
    bot.register_next_step_handler(message, lambda m: handle_promocode(m, bot, user))


def handle_promocode(message, bot, user: EntityUser):
    value = promocodes.redeem_promocode(user, message.text)
    if value != 0:
        bot.send_message(message.chat.id, f'Начислил вам {value}¢')
    else:
        bot.send_message(message.chat.id, 'Теперь вы администратор.')
