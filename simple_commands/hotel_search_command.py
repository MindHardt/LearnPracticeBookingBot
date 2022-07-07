from telebot import types

import webparser
from simple_commands.abstract_simple_command import AbstractSimpleCommand


class HotelSearchCommand(AbstractSimpleCommand):

    def get_name(self):
        return 'Найти отель'

    def execute(self, message, bot):
        bot.send_message(message.chat.id, 'Введите город,checkin,checkout (dd.mm.yyyy):')
        bot.register_next_step_handler(message, lambda m: self.handle_hotel_search(m, bot))

    def handle_hotel_search(self, message, bot):
        try:
            args = message.text.split(',')
            city = args[0]
            checkin = args[1]
            checkout = args[2]
            bparser = webparser.BookingParser()
            hotels_data = bparser.parse(city, checkin, checkout, 10, message.chat.id, bot.token)

            response = ''
            for s in hotels_data:
                response += f"{s['name']} {s['rate']}\n"

            bot.send_message(message.chat.id, response)
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка в вводе данных: `{e}`")

    