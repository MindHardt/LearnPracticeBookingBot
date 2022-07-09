import telebot
from commands import draw_map_command, hotel_search_command, redeem_promocode_command, create_promocode_command, \
    register_command, login_command, logout_command
from controller import parser_controller
from utilities import markup_generator

with open('token.txt') as file:
    token = file.readline()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для доступа к функционалу используйте /menu')


@bot.message_handler(commands=['menu'])
def menu_message(message):
    pass


@bot.message_handler(content_types='text')
def message_non_command_handle(message):
    try:
        call = message.text
        if call == "Точка на карте":
            draw_map_command.execute(message, bot)
        elif call == "Найти отель":
            hotel_search_command.execute(message, bot)
        elif call == "Использовать промокод":
            redeem_promocode_command.execute(message, bot)
        elif call == "Создать промокод":
            create_promocode_command.execute(message, bot)
        elif call == "Зарегистрироваться":
            register_command.execute(message, bot)
        elif call == "Войти":
            login_command.execute(message, bot)
        elif call == "Выйти":
            logout_command.execute(message, bot)

    except Exception as e:
        bot.send_message(message.chat.id, e.__str__())


@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def listed_handle(call):
    try:
        direction = call.data[5:]
        reply = parser_controller.update_paginated_message(call.message.chat.id, direction)
        if reply == '':
            return
        markup = markup_generator.get_pagination_markup()
        bot.edit_message_text(reply, call.message.chat.id, call.message.message_id, reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')


print('Started!')
bot.infinity_polling()
