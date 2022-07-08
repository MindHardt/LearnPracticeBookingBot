import datetime
import uuid

from database import table_requests
from database.entity_request import EntityRequest
from controller import authentificator, parser_controller


def execute(message, bot):
    bot.send_message(message.chat.id, 'Введите город,checkin,checkout (dd.mm.yyyy):')
    bot.register_next_step_handler(message, lambda m: handle_hotel_search(m, bot))


def handle_hotel_search(message, bot):
    try:
        args = message.text.split(',')
        city = args[0]
        checkin = args[1]
        checkout = args[2]

        if checkin is not datetime.date or checkout is not datetime.date or checkin >= checkout:
            raise TypeError

        request = EntityRequest()
        request.unique_id = uuid.uuid4()
        request.date_request = datetime.datetime.now()
        request.user_id = authentificator.get_user(message.chat.id)
        request.date_arrive = checkin
        request.date_depart = checkout
        request.destination = city
        
        table_requests.save(request)

        parser_controller.queue_parse(request, bot, message.chat.id)

        # booking_parser = webparser.BookingParser()
        # hotels_data = booking_parser.parse(city, checkin, checkout, 10, message.chat.id, bot.token)
        #
        # response = ''
        # for s in hotels_data:
        #     response += f"{s['name']} {s['rate']}\n"
        #     bot.send_message(message.chat.id, response)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка в вводе данных: `{e}`")

    