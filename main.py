import telebot
from PIL.Image import Image
from geopy.geocoders import Nominatim
from staticmap import StaticMap, CircleMarker
from telebot import types

with open('token.txt') as file:
    token = file.readline()

bot = telebot.TeleBot(token)


starred = []
user_data = dict()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для доступа к функционалу используйте /menu')


@bot.message_handler(commands=['menu'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # BUTTONS
    map_pointer_button = types.KeyboardButton('Точка на карте')
    markup.add(map_pointer_button)

    clear_filters_button = types.KeyboardButton('Очистить фильтры')
    markup.add(clear_filters_button)

    add_filter_button = types.KeyboardButton('Добавить фильтр')
    markup.add(add_filter_button)

    list_filters_button = types.KeyboardButton('Список фильтров')
    markup.add(list_filters_button)

    add_star_button = types.KeyboardButton('Сохранить в избранное')
    markup.add(add_star_button)

    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_noncommand_handle(message):
    if message.text == 'Точка на карте':
        bot.send_message(message.chat.id, 'Введите координаты или адрес')
        bot.register_next_step_handler(message, handle_coordinates)

    elif message.text == 'Добавить фильтр':
        bot.send_message(message.chat.id, 'Введите фильтр')
        bot.register_next_step_handler(message, add_filter)

    elif message.text == 'Список фильтров':
        filters = user_data.get(message.chat.id)
        bot.send_message(message.chat.id, f'Список фильтров:\n{filters}')

    elif message.text == 'Очистить фильтры':
        user_data.pop(message.chat.id)
        bot.send_message(message.chat.id, 'Очистил список фильтров')

    elif message.text == 'Сохранить в избранное':
        bot.send_message(message.chat.id, 'Введите url')
        bot.register_next_step_handler(message, add_filter)


def handle_coordinates(message):
    coordinates = message.text
    locator = Nominatim(user_agent="IIT2022BookingBot")
    try:
        location = locator.geocode(coordinates)

        lon = location.longitude
        lat = location.latitude

        response = f"{location.address}\n\n{lat}, {lon}"
        bot.send_message(message.chat.id, response)

        maps_link = f"https://yandex.ru/maps/?ll={lon}%2C{lat}&mode=whatshere&whatshere%5Bpoint%5D={lon}%2C{lat}&whatshere%5Bzoom%5D=18.75&z=20"
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Ссылка на яндекс-карты", url=maps_link)
        markup.add(button1)

        img = create_map(location.latitude, location.longitude)
        bot.send_chat_action(message.chat.id, 'upload_photo')
        bot.send_photo(message.chat.id, img, reply_to_message_id=message.id, reply_markup=markup)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "Что-то пошло не так!!!")


def add_filter(message):
    if user_data.get(message.chat.id) is None:
        user_data[message.chat.id] = []

    user_data[message.chat.id].append(message.text)

    bot.send_message(message.chat.id, f'Добавил `{message.text}` в список фильтров')


def add_star(message):
    starred.append(message.text)
    bot.send_message(message.chat.id, f'Добавил {message.text} в избранное!')


def create_map(lat, long) -> Image:
    m = StaticMap(1024, 1024, 10)
    m.add_marker(CircleMarker((long, lat), "red", 5))
    return m.render()


print('Started!')
bot.infinity_polling()
