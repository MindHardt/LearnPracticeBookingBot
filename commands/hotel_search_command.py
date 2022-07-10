import datetime
import uuid

from database import table_requests
from controller import authentificator, parser_controller, config_controller
from database.table_requests import EntityRequest


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if user is None:
        raise Exception('Вы не авторизованы!')
    price = int(config_controller.get_value('hotel_search_price'))
    if user.balance < price:
        raise Exception(f'У вас недостаточно средств! (Нужно {price})')
    user.balance -= price
    user.update_balance()
    bot.send_message(message.chat.id, 'Введите город, дату въезда и выезда, каждое с новой строки (dd.mm.yyyy):')
    bot.register_next_step_handler(message, lambda m: handle_hotel_search(m, bot, user))


def handle_hotel_search(message, bot, user):
    try:
        args = message.text.split('\n')
        city = args[0]
        checkin = datetime.datetime.strptime(args[1], '%d.%m.%Y').date()
        checkout = datetime.datetime.strptime(args[2], '%d.%m.%Y').date()

        if checkin >= checkout:
            raise TypeError('Неверные даты!')

        request = EntityRequest()
        request.unique_id = uuid.uuid4().__str__()
        request.date_request = datetime.datetime.now()
        request.user_id = user.unique_id
        request.date_arrive = checkin
        request.date_depart = checkout
        request.destination = city

        request.save()

        parser_controller.queue_parse(request, bot, message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

    