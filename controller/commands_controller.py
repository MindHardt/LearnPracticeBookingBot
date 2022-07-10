import telebot.types

from commands import draw_map_command, hotel_search_command, redeem_promocode_command, create_promocode_command, \
    register_command, login_command, logout_command, info_command, set_config_command, view_config_command
from controller import authentificator
from database import table_admins


def handle_command(message, bot):
    try:
        call = message.text
        if call == "Точка на карте":
            draw_map_command.execute(message, bot)
        elif call == "Найти отель":
            hotel_search_command.execute(message, bot)
        elif call == "Использовать промокод":
            redeem_promocode_command.execute(message, bot)
        elif call == "Зарегистрироваться":
            register_command.execute(message, bot)
        elif call == "Войти":
            login_command.execute(message, bot)
        elif call == "Выйти":
            logout_command.execute(message, bot)
        elif call == "Инфо":
            info_command.execute(message, bot)
            # ADMIN COMMANDS
        elif call.startswith("=setconfig"):
            set_config_command.execute(message, bot)
        elif call == "=viewconfig":
            view_config_command.execute(message, bot)
        elif call == "=create_promocode":
            create_promocode_command.execute(message, bot)

    except Exception as e:
        bot.send_message(message.chat.id, e.__str__())


def get_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    markup = telebot.types.ReplyKeyboardMarkup()
    markup.add(telebot.types.KeyboardButton('Точка на карте'))
    markup.add(telebot.types.KeyboardButton('Найти отель'))
    markup.add(telebot.types.KeyboardButton('Использовать промокод'))
    markup.add(telebot.types.KeyboardButton('Зарегистрироваться'))
    markup.add(telebot.types.KeyboardButton('Войти'))
    markup.add(telebot.types.KeyboardButton('Выйти'))
    markup.add(telebot.types.KeyboardButton('Инфо'))

    return markup
