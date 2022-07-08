from database.entity_user import EntityUser
import sqlite3

connection = sqlite3.connect('h.db')
cursor = connection.cursor()


def auth(login: str, password_hash: int) -> EntityUser:
    """Tries to find a user with specified login and password hash in database and returns it if it exists."""
    # TODO: auth(login: str, password_hash: int)
    pass


def try_register(user: EntityUser) -> bool:
    """Tries to register user with specified data and returns True if succeeds and False otherwise. It may fail due to repeating login."""
    # TODO: try_register(user: EntityUser)
    pass


def __create_table__():
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("CREATE TABLE IF NOT EXISTS EntityUser(unique_id VARCHAR(36) PRIMARY KEY, "
                       "name VARCHAR(36), balance INTEGER, login VARCHAR(36) UNIQUE, "
                       "password_hash INTEGER")
    connection.commit()
