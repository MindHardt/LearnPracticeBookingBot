from database.entity_user import EntityUser

logged_in = dict()


def login(user: EntityUser, chat_id):
    logged_in[chat_id] = user


def get_user(chat_id) -> EntityUser():
    """Gets user connected to this chat_id. Throws KeyError is none is found"""
    user = logged_in.get(chat_id)
    if user is None:
        raise KeyError('Пользователь не авторизован!')
    return user
