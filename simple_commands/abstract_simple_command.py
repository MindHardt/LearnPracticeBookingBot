from abc import ABCMeta, abstractmethod


class AbstractSimpleCommand:
    __metaclass__ = ABCMeta

    name = str

    @abstractmethod
    def execute(self, message, bot):
        """Executes this SimpleCommand with specified message and telebot instances"""

    @abstractmethod
    def get_name(self):
        """Gets name of this command"""
