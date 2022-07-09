import telebot
from commands import draw_map_command, hotel_search_command, redeem_promocode_command, create_promocode_command, \
    register_command, login_command, logout_command

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


print('Started!')
bot.infinity_polling()
