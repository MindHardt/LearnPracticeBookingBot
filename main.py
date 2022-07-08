import telebot

from commands import map_pointer_command, hotel_search_command

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
    call = message.text
    if call == "Точка на карте":
        bot.register_next_step_handler(message, lambda m: map_pointer_command.execute(m, bot))
    elif call == "Найти отель":
        bot.register_next_step_handler(message, lambda m: hotel_search_command.execute(m, bot))


print('Started!')
bot.infinity_polling()
