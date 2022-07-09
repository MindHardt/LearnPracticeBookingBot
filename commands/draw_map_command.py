import os
import uuid

import PIL.Image
from PIL.Image import Image
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
from geopy import Nominatim
from staticmap import StaticMap, CircleMarker, IconMarker


def execute(message, bot):
    bot.send_message(message.chat.id, 'Введите координаты или адрес, каждый с новой строки')
    bot.register_next_step_handler(message, lambda m: handle_coordinates(m, bot))


def handle_coordinates(message, bot):
    coordinates_texts = message.text.split('\n')
    locator = Nominatim(user_agent="IIT2022BookingBot")
    try:
        coordinates = []
        for text in coordinates_texts:
            location = locator.geocode(text)
            coordinates.append((location.longitude, location.latitude, location.address))

        bot.send_message(message.chat.id, 'Начинаю рисовать карту...')
        # maps_link = f"https://yandex.ru/maps/?ll={lon}%2C{lat}&mode=whatshere&whatshere%5Bpoint%5D={lon}%2C{lat}&whatshere%5Bzoom%5D=18.75&z=10"
        # markup = types.InlineKeyboardMarkup()
        # button1 = types.InlineKeyboardButton("Ссылка на яндекс-карты", url=maps_link)
        # markup.add(button1)

        # response = f"{location.address}\n\n{lat}, {lon}"
        # bot.send_message(message.chat.id, response, reply_markup=markup)
        try:
            img = create_map(coordinates)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            bot.send_photo(message.chat.id, img, reply_to_message_id=message.id)
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка при отправке карты: `{e}`")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: `{e}`")


def create_map(coordinates_list: list) -> Image:
    m = StaticMap(1024, 1024, 10)
    marker_temp_files = []
    for point in coordinates_list:
        coordinates = (point[0], point[1])

        marker_temp_file = create_marker(point[2])
        marker_temp_files.append(marker_temp_file)

        m.add_marker(CircleMarker(coordinates, "red", 10))
        m.add_marker(IconMarker(coordinates, marker_temp_file, 5, 5))
    render = m.render()

    for marker_temp_file in marker_temp_files:
        os.remove(marker_temp_file)

    return render


def create_marker(text: str) -> str:
    """Creates an IconMarker with specified text and returns path to it."""
    img = PIL.Image.new(mode="RGBA", size=(400, 50))
    fnt = truetype('arial.ttf', 16)
    draw = Draw(img)
    draw.text((10, 15), text, font=fnt, fill="red")
    img_name = uuid.uuid4().__str__() + '.png'
    img.save(img_name)
    return img_name

