from queue import Queue

__queue = Queue(-1)


def queue_parse(message, bot, chat_id):
    if __queue.empty():
        __queue.put((message, bot, chat_id))
        initiate_parse()
    else:
        __queue.put((message, bot, chat_id))
        bot.send_message(chat_id, f'Перед вами в очереди примерно {__queue.qsize()} человек. Ожидайте.')
    print(f'Added {message.text} to parse queue')


def initiate_parse() -> []:
    """Adds parsing to the queue and keeps user informed about the progress"""
    current = __queue.get()
    message = current[0]
    bot = current[1]
    chat_id = current[2]
    print(f'Initiated parse of {message.text} to parse queue')
    bot.send_message(chat_id, 'Начинаю поиск')
    # ЗДЕСЬ НАЧИНАЕМ ПАРСИНГ ПО РЕКВЕСТУ
    return None
