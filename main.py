from PIL.Image import Image
from geopy.geocoders import Nominatim
from staticmap import StaticMap, CircleMarker
from telebot import types

import filter_menu
import telebot

with open('token.txt') as file:
    token = file.readline()

bot = telebot.TeleBot(token)
filter_menu.bot = bot


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для доступа к функционалу используйте /menu')


@bot.message_handler(commands=['menu'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # BUTTONS
    map_pointer_button = types.KeyboardButton('Точка на карте')
    markup.add(map_pointer_button)

    add_filter_button = types.KeyboardButton('Настроить фильтры')
    markup.add(add_filter_button)

    add_star_button = types.KeyboardButton('Сохранить в избранное')
    markup.add(add_star_button)

    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(commands=['filters'])
def goto_filters(message):
    bot.send_message(message.chat.id, 'Настраиваем фильтры. Чтобы вернуться в меню можете использовать /filters', reply_markup=filter_menu.get_markup())


@bot.message_handler(content_types='text')
def message_noncommand_handle(message):
    if message.text == 'Точка на карте':
        bot.send_message(message.chat.id, 'Введите координаты или адрес')
        bot.register_next_step_handler(message, handle_coordinates)

    elif message.text == 'Настроить фильтры':
        goto_filters(message)

    elif message.text in filter_menu.filter_triggers:
        filter_menu.message_filters_handle(message)

    elif message.text == 'Назад':
        button_message(message)


def handle_coordinates(message):
    coordinates = message.text
    locator = Nominatim(user_agent="IIT2022BookingBot")
    try:
        location = locator.geocode(coordinates)

        lon = location.longitude
        lat = location.latitude

        maps_link = f"https://yandex.ru/maps/?ll={lon}%2C{lat}&mode=whatshere&whatshere%5Bpoint%5D={lon}%2C{lat}&whatshere%5Bzoom%5D=18.75&z=10"
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Ссылка на яндекс-карты", url=maps_link)
        markup.add(button1)

        response = f"{location.address}\n\n{lat}, {lon}"
        bot.send_message(message.chat.id, response, reply_markup=markup)
        try:
            img = create_map(location.latitude, location.longitude)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, img, reply_to_message_id=message.id)
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при отправке карты: `{e}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: `{e}`")


def create_map(lat, long) -> Image:
    m = StaticMap(1024, 1024, 10)
    m.add_marker(CircleMarker((long, lat), "red", 5))
    return m.render()


print('Started!')
bot.infinity_polling()
