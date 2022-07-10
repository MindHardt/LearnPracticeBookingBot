import telebot
from telebot import types

from commands.draw_map_command import create_map, send_map

__paginated_messages = dict()


def create_hotel_view(chat_id, hotels: list, bot):

    __paginated_messages[chat_id] = (hotels, 2, set())
    # all the hotels, current page, current filters
    response = update_page(chat_id, 'b')
    paginator = get_pagination_markup()

    bot.send_message(chat_id, response, reply_markup=paginator)


def handle_pagination_callback(call, bot):
    try:
        direction = call.data[5:]
        if direction == 'm':

            hotels = __paginated_messages[call.message.chat.id][0]
            coordinates = []

            for hotel in hotels:
                coordinates.append((hotel['longitude'], hotel['latitude'], f"{hotel['rate']} {hotel['name']}"))

            map_img = create_map(coordinates)
            send_map(bot, call.message.chat.id, map_img)
        else:
            reply = update_page(call.message.chat.id, direction)
            if reply == '':
                return
            markup = get_pagination_markup()
            bot.edit_message_text(reply, call.message.chat.id, call.message.message_id, reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')


def update_page(chat_id: int, direction: str) -> str:
    try:
        data = __paginated_messages[chat_id]
    except KeyError:
        raise Exception('Данное меню неактивно. Одновременно активно только одно меню, старые меню также периодически удаляются.')
    hotels = data[0]
    page = data[1]
    if direction == 'f':
        if page >= len(hotels):
            return ''
        page += 1
    else:
        if data[1] <= 1:
            return ''
        page -= 1
    hotel = hotels[page - 1]
    response = f"Отель № {page}/{len(hotels)}\n{format_hotel(hotel)}"
    __paginated_messages[chat_id] = (hotels, page)
    return response


def format_hotel(data) -> str:
    tags = sorted(list(set(data['tags'])))
    tag_list = str()

    for tag in tags:
        tag_list += f'{tag}\n'
    return f"{data['name']}\n{data['rate']}\n\nТеги:\n{tag_list}"


def get_pagination_markup() -> telebot.types.InlineKeyboardMarkup:
    paginator = types.InlineKeyboardMarkup(row_width=2)
    backward_button = types.InlineKeyboardButton('<', callback_data='page_b')
    forward_button = types.InlineKeyboardButton('>', callback_data='page_f')
    map_button = types.InlineKeyboardButton('Создать карту', callback_data='page_m')
    paginator.add(backward_button, forward_button, map_button)

    return paginator


def get_filter_button(filter_text: str, is_disable_button: bool):
    sign = '-' if is_disable_button else '+'
    keyword = 'disable' if is_disable_button else 'enable'
    return types.InlineKeyboardButton(f'{sign} {filter_text}', callback_data=f'filter_{keyword}_{filter_text}')
