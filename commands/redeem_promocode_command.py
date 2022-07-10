import telebot.formatting

from controller import authentificator, promocodes_controller
from database.table_users import EntityUser


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    bot.send_message(message.chat.id, 'Введите промокод')
    bot.register_next_step_handler(message, lambda m: handle_promocode(m, bot, user))


def handle_promocode(message, bot, user: EntityUser):
    try:
        value = promocodes_controller.redeem_promocode(user, message.text)
        if value != 0:
            bot.send_message(message.chat.id, f'Начислил вам {value}¢')
        else:
            bot.send_message(message.chat.id, 'Теперь вы администратор.')
    except Exception as e:
        errmsg = telebot.formatting.mcode(e.__str__())
        bot.send_message(message.chat.id, f'Произошла ошибка: {errmsg}')
