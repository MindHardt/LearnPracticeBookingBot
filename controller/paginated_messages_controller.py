import telebot
from telebot import types

from commands.draw_map_command import create_map, send_map

__paginated_messages = dict()


def create_hotel_view(chat_id, hotels: list, bot):

    __paginated_messages[chat_id] = (hotels, 2, set(), hotels)
    # all the hotels, current page, current filters
    response = update_page(chat_id, 'b')
    paginator = get_pagination_markup(chat_id)

    bot.send_message(chat_id, response, reply_markup=paginator)


def handle_pagination_callback(call, bot):
    try:
        direction = call.data[5:]
        if direction == 'm':

            hotels = __paginated_messages[call.message.chat.id][3]
            coordinates = []

            for hotel in hotels:
                coordinates.append((hotel['longitude'], hotel['latitude'], f"{hotel['rate']} {hotel['name']}"))

            map_img = create_map(coordinates)
            send_map(bot, call.message.chat.id, map_img)
        elif direction.startswith('f_'):
            filters = __paginated_messages[call.message.chat.id][2]
            current_filter = direction[2:]

            filters.add(current_filter)

            __paginated_messages[call.message.chat.id][3] = get_suiting_hotels(__paginated_messages[0], filters)
            available_filters = get_available_filters(call.message.chat.id)

            markup = get_pagination_markup(available_filters)
            reply = update_page(call.message.chat.id, '')
            bot.edit_message_text(reply, call.message.chat.id, call.message.message_id, reply_markup=markup)
        else:
            reply = update_page(call.message.chat.id, direction)
            if reply == '':
                return

            all_filters = get_all_tags(__paginated_messages[call.message.chat.id][3])

            applied_filters = __paginated_messages[call.message.chat.id][2]

            available_filters = all_filters.difference(applied_filters)
            markup = get_pagination_markup(available_filters)
            bot.edit_message_text(reply, call.message.chat.id, call.message.message_id, reply_markup=markup)
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')


def update_page(chat_id: int, direction: str) -> str:
    try:
        data = __paginated_messages[chat_id]
    except KeyError:
        raise Exception('Данное меню неактивно. Одновременно активно только одно меню, старые меню также периодически удаляются.')
    hotels = data[3]
    page = data[1]
    if direction == 'f':
        if page >= len(hotels):
            return ''
        page += 1
    elif direction == 'b':
        if data[1] <= 1:
            return ''
        page -= 1
    if page > len(hotels):
        page = 1
    hotel = hotels[page - 1]
    response = f"Отель № {page}/{len(hotels)}\n{format_hotel(hotel)}"
    __paginated_messages[chat_id] = (hotels, page, __paginated_messages[chat_id][2], __paginated_messages[chat_id][3])
    return response


def get_all_tags(hotels: list) -> set:
    all_filters = set()
    for hotel in hotels:
        for current_filter in hotel['tags']:
            all_filters.add(current_filter)
    return all_filters


def get_suiting_hotels(hotels: list, filters: set) -> list:
    suiting_hotels = []
    for hotel in hotels:
        tags_set = set(hotel['data'])
        if len(tags_set.intersection(filters)) == len(filters):
            suiting_hotels.append(hotel)
    return suiting_hotels


def get_available_filters(chat_id):
    hotels = __paginated_messages[chat_id]
    all_tags = get_all_tags(hotels[0])
    current_filters = hotels[2]
    return all_tags.difference(current_filters)


def format_hotel(data) -> str:
    tags = sorted(list(set(data['tags'])))
    tag_list = str()

    for tag in tags:
        tag_list += f'{tag}\n'
    return f"Теги: {tag_list}\n\n{data['name']}\n{data['rate']}\n\nСсылка:{data['url']}"


def get_pagination_markup(chat_id) -> telebot.types.InlineKeyboardMarkup:
    paginator = types.InlineKeyboardMarkup(row_width=2)
    backward_button = types.InlineKeyboardButton('<', callback_data='page_b')
    forward_button = types.InlineKeyboardButton('>', callback_data='page_f')
    map_button = types.InlineKeyboardButton('Создать карту', callback_data='page_m')
    paginator.add(backward_button, forward_button, map_button)

    return paginator

    available_filters = get_available_filters(chat_id)
    for curr_filter in available_filters:
        button = types.InlineKeyboardButton(curr_filter, callback_data=f'page_f_{curr_filter}')
        paginator.add(button)

    return paginator
