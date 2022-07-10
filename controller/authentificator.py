from database.table_users import EntityUser

logged_in = dict()


def auth(user: EntityUser, chat_id):
    logged_in[chat_id] = user


def logout(chat_id) -> EntityUser:
    """Logs user out of specified channel and returns it. If none was found, returns None"""
    return logged_in.pop(chat_id, None)


def get_user(chat_id) -> EntityUser():
    """Gets user connected to this chat_id or returns None if there is none"""
    return logged_in.get(chat_id, None)
