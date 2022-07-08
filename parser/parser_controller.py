import telebot


def initiate_parse(query, bot: telebot.Telebot, chat_id):
    """Adds parsing to the queue and keeps user informed about the progress"""
    # TODO: initiate_parse(query, bot: telebot.Telebot, chat_id)
    # Как я себе это вижу: сюда передаем запрос (query), id чата и клиент телеграма (bot). По ходу процесса вызывай bot.send_message(chat_id, 'Здесь текст который передаем').
