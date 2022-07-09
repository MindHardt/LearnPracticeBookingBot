from queue import Queue
from telebot import types

import webparser
from controller.paginated_messages_controller import create_hotel_view

__queue = Queue(-1)


def queue_parse(request, bot, chat_id):
    if __queue.empty():
        __queue.put((request, bot, chat_id))
        initiate_parse()
    else:
        __queue.put((request, bot, chat_id))
        bot.send_message(chat_id, f'Перед вами в очереди примерно {__queue.qsize()} человек. Ожидайте.')
    print(f'Added {request.destination} to parse queue')


def initiate_parse():
    """Adds parsing to the queue and keeps user informed about the progress"""
    current = __queue.get()
    request = current[0]
    bot = current[1]
    chat_id = current[2]
    print(f'Initiated parse of {request.destination} to parse queue')
    bot.send_message(chat_id, 'Начинаю поиск')

    booking_parser = webparser.BookingParser()

    hotels_data = booking_parser.parse(request.destination, request.date_arrive, request.date_depart, 10, chat_id, bot.token)
    # hotels_data = []
    # hotel1 = {"name": "name1", "rate": 5}
    # hotel2 = {"name": "name2", "rate": 4}
    # hotel3 = {"name": "name3", "rate": 3}
    # hotels_data.append(hotel1)
    # hotels_data.append(hotel2)
    # hotels_data.append(hotel3)

    create_hotel_view(chat_id, hotels_data, bot)
    # response = ''
    # for s in hotels_data:
    #     response += f"{s['name']} {s['rate']}\n"
    # bot.send_message(chat_id, response)



