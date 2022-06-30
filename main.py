import io

import telebot
import geopy
import staticmap
from PIL.Image import Image
from geopy.geocoders import Nominatim
from staticmap import StaticMap, IconMarker, CircleMarker
from telebot import types

with open('token.txt') as file:
    token = file.readline()

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Для доступа к функционалу используйте /menu')


@bot.message_handler(commands=['menu'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Точка на карте")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_coordinates(message):
    if message.text == "Точка на карте":
        bot.send_message(message.chat.id, 'Введите координаты или адрес')
        bot.register_next_step_handler(message, handle_coordinates)


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


def create_map(lat, long) -> Image:
    m = StaticMap(1024, 1024, 10)
    m.add_marker(CircleMarker((long, lat), "red", 5))
    return m.render()


print('Started!')
bot.infinity_polling()
