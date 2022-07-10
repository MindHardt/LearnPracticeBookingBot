import telebot
from controller import paginated_messages_controller, commands_controller

with open('token.txt') as file:
    token = file.readline()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для доступа к функционалу используйте /menu')


@bot.message_handler(commands=['menu'])
def menu_message(message):
    bot.send_message(message.chat.id, 'Меню перед вами:', reply_markup=commands_controller.get_keyboard())


@bot.message_handler(content_types='text')
def message_non_command_handle(message):
    commands_controller.handle_command(message, bot)


@bot.callback_query_handler(func=lambda call: call.data.startswith('page_'))
def listed_handle(call):
    paginated_messages_controller.handle_pagination_callback(call, bot)


print('Started!')
bot.infinity_polling()
