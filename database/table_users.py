from database.entity_user import EntityUser


def auth(login: str, password_hash: int) -> EntityUser:
    """Tries to find a user with specified login and password hash in database and returns it if it exists."""
    # TODO: auth(login: str, password_hash: int)
    pass


def try_register(user: EntityUser) -> bool:
    """Tries to register user with specified data and returns True if succeeds and False otherwise. It may fail due to repeating login."""
    # TODO: try_register(user: EntityUser)
    pass