import datetime

import webparser
from controller import authentificator, config_controller
from database.table_favorites import FavoriteData


def execute(message, bot):
    user = authentificator.get_user(message.chat.id)
    if user is None:
        raise Exception('Вы не авторизованы!')
    price = int(config_controller.get_value('hotel_search_price'))
    if user.balance < price:
        raise Exception(f'У вас недостаточно средств! (Нужно {price})')
    user.balance -= price
    user.update_balance()
    bot.send_message(message.chat.id, 'Введите ссылку на отель:')
    bot.register_next_step_handler(message, lambda m: handle_track_input(m, bot))


def handle_track_input(message, bot):
    try:
        url = message.text
        # print(f'Trying to fetch user with login {login} and password_hash {password}')
        raw_data = dict()
        data = FavoriteData()
        parsers = [webparser.BookingParser(), webparser.YandexParser()]
        for parser in parsers:
            output = parser.__get_hotel_data(url)
            if output is not None and not output.empty():
                raw_data = output
        data.price = raw_data['rate']
        data.time = datetime.datetime.now()
        # data.favorite_id
        bot.send_message(message.chat.id, 'lorem ipsum dolorem sit amet')

    except Exception as e:
        bot.send_message(message.chat.id, f'Произошла ошибка: {e}')

