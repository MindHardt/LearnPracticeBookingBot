from abc import ABCMeta, abstractmethod
from telebot import types


class AbstractMenu:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self) -> str:
        """Gets name of this menu, usually a name of button which redirects to it."""

    @abstractmethod
    def get_greetings(self) -> str:
        """Gets a greeting message that shows when this menu appears"""

    @abstractmethod
    def get_triggers(self) -> []:
        """Keywords that help menu recognize calls to its own"""

    @abstractmethod
    def handle_message(self, message, bot):
        """Handler for messages that are recognized as this menus"""

    def jump(self, message, bot):
        bot.send_message(message.chat.id, self.get_greetings(), reply_markup=self.get_markup())
        print(f'Adressed {message.chat.id} to {self.__str__()}')
        """Addresses user to this Menu"""

    def get_markup(self) -> types.ReplyKeyboardMarkup:
        """Gets keyboard markup for this Menu"""
        buttons = []
        for trigger in self.get_triggers():
            buttons.append(types.KeyboardButton(trigger))

        markup = types.ReplyKeyboardMarkup()
        for button in buttons:
            markup.add(button)
        markup.add(types.KeyboardButton('Меню'))
        return markup
