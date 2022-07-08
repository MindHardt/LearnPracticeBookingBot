import datetime
import uuid

from database import table_requests
from database.entity_request import EntityRequest
from controller import authentificator, parser_controller


def execute(message, bot):
    bot.send_message(message.chat.id, 'Введите город, дату въезда и выезда через пробел (dd.mm.yyyy):')
    bot.register_next_step_handler(message, lambda m: handle_hotel_search(m, bot))


def handle_hotel_search(message, bot):
    try:
        args = message.text.split(' ')
        city = args[0]
        checkin = datetime.datetime.strptime(args[1], '%d.%m.%Y').date()
        checkout = datetime.datetime.strptime(args[2], '%d.%m.%Y').date()

        if checkin >= checkout:
            raise TypeError('Неверные даты!')

        request = EntityRequest()
        request.unique_id = uuid.uuid4()
        request.date_request = datetime.datetime.now()
        request.user_id = authentificator.get_user(message.chat.id)
        request.date_arrive = checkin
        request.date_depart = checkout
        request.destination = city

        table_requests.save(request)

        parser_controller.queue_parse(request, bot, message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e.__str__()}')

    