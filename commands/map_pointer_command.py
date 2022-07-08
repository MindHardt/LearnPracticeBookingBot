from PIL.Image import Image
from geopy import Nominatim
from staticmap import StaticMap, CircleMarker
from telebot import types


def execute(message, bot):
    bot.send_message(message.chat.id, 'Введите координаты или адрес')
    bot.register_next_step_handler(message, lambda m: handle_coordinates(m, bot))

def handle_coordinates(message, bot):
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
