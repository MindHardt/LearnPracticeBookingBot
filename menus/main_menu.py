from menus.abstract_menu import AbstractMenu
from menus.filter_menu import FilterMenu
from simple_commands.map_pointer_command import MapPointerCommand
from simple_commands.hotel_search_command import HotelSearchCommand


class MainMenu(AbstractMenu):

    def handle_message(self, message, bot):
        if message.text == 'Сука':
            bot.send_message(message.chat.id, 'Сам сука')

    def get_triggers(self) -> []:
        return [MapPointerCommand().get_name(), 'Сука', FilterMenu().get_name(), HotelSearchCommand().get_name()]

    def get_greetings(self) -> str:
        return 'Выберите что вам нужно'

    def get_name(self) -> str:
        return 'Меню'
