import telebot
from menus.filter_menu import FilterMenu
from menus.main_menu import MainMenu
from simple_commands.map_pointer_command import MapPointerCommand
from simple_commands.hotel_search_command import HotelSearchCommand

with open('token.txt') as file:
    token = file.readline()

bot = telebot.TeleBot(token)
menus = [FilterMenu(), MainMenu()]
commands = [MapPointerCommand(), HotelSearchCommand()]
trigger_callbacks = dict()

for menu in menus:
    handler = lambda m, b: menu.handle_message(m, b)
    for trigger in menu.get_triggers():
        trigger_callbacks[trigger] = handler

for command in commands:
    trigger_callbacks[command.get_name()] = lambda m, b: command.execute(m, b)

for menu in menus:
    name = menu.get_name()
    jump_func = lambda m, b: menu.jump(m, b)
    trigger_callbacks[name] = jump_func

print(f'Triggers: {trigger_callbacks}')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для доступа к функционалу используйте /menu')


@bot.message_handler(commands=['menu'])
def menu_message(message):
    MainMenu().jump(message, bot)


@bot.message_handler(content_types='text')
def message_non_command_handle(message):
    trigger_callbacks[message.text].__call__(message, bot)


print('Started!')
bot.infinity_polling()
