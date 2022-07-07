from menus.abstract_menu import AbstractMenu


class FilterMenu(AbstractMenu):

    user_filters = dict()

    def get_name(self) -> str:
        return 'Настроить фильтры'

    def get_triggers(self) -> []:
        return ['Добавить фильтр', 'Список фильтров', 'Очистить фильтры']

    def handle_message(self, message, bot):
        triggers = self.get_triggers()
        if message.text == triggers[0]:
            bot.send_message(message.chat.id, 'Введите желаемый фильтр')
            bot.register_next_step_handler(message, lambda m: self.add_filter(m, bot))

        elif message.text == triggers[1]:
            filters = self.get_filters(message.chat.id)
            bot.send_message(message.chat.id, f'Ваш список фильтров:\n{filters}')

        elif message.text == triggers[2]:
            self.user_filters.pop(message.chat.id)
            bot.send_message(message.chat.id, 'Очистил ваш список фильтров.')

    def add_filter(self, message, bot):
        try:
            self.user_filters[message.chat.id]
        except KeyError:
            self.user_filters[message.chat.id] = []
        self.user_filters[message.chat.id].append(message.text)
        bot.send_message(message.chat.id, f'Добавил {message.text} в список фильтров')

    def get_filters(self, chat_id) -> str:
        try:
            return self.user_filters[chat_id]
        except KeyError:
            return 'У вас нет фильтров ¯\\_(ツ)_/¯'

    def get_greetings(self) -> str: return 'Выберите что хотите сделать с фильтрами'

