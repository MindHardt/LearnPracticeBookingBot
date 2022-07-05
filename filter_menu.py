import telebot.types

add_filter_button_name = 'Добавить фильтр'
list_filters_button_name = 'Список фильтров'
clear_filters_button_name = 'Очистить фильтры'
filter_triggers = [add_filter_button_name, list_filters_button_name, clear_filters_button_name]

user_filters = dict()
bot = None


def message_filters_handle(message):
    if message.text == add_filter_button_name:
        bot.send_message(message.chat.id, 'Введите желаемый фильтр')
        bot.register_next_step_handler(message, add_filter)

    elif message.text == list_filters_button_name:
        filters = get_filters(message.chat.id)
        bot.send_message(message.chat.id, f'Ваш список фильтров:\n{filters}')

    elif message.text == clear_filters_button_name:
        user_filters.pop(message.chat.id)
        bot.send_message(message.chat.id, 'Очистил ваш список фильтров.')


def add_filter(message):
    try:
        user_filters[message.chat.id]
    except KeyError:
        user_filters[message.chat.id] = []
    user_filters[message.chat.id].append(message.text)
    bot.send_message(message.chat.id, f'Добавил {message.text} в список фильтров')


def get_filters(chat_id) -> str:
    try:
        return user_filters[chat_id]
    except KeyError:
        return 'У вас нет фильтров ¯\\_(ツ)_/¯'


def get_markup() -> telebot.types.ReplyKeyboardMarkup:
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_filter_button = telebot.types.KeyboardButton(add_filter_button_name)
    list_filters_button = telebot.types.KeyboardButton(list_filters_button_name)
    clear_filters_button = telebot.types.KeyboardButton(clear_filters_button_name)
    back_menu = telebot.types.KeyboardButton('Назад')

    markup.add(add_filter_button, list_filters_button, clear_filters_button, back_menu)
    return markup

