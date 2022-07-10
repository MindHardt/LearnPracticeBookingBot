import sqlite3
import datetime
import hashlib
import uuid

from controller import config_controller
from database import table_admins


class EntityUser:
    unique_id = str()  # VARCHAR(36), PK
    name = str()  # VARCHAR(36)
    balance = 0  # INTEGER
    login = str()  # VARCHAR(36), UNIQUE
    password_hash = str()  # TEXT
    is_admin = bool()  # NOT IN TABLE
    time_register = datetime.datetime  # DATETIME

    def register(self):
        """Tries to register user with specified data."""
        __create_table__()
        query = "insert into 'EntityUser'(unique_id, name, balance, login, password_hash, time_register) values(?,?,?,?,?,?);"
        connection = sqlite3.connect('h.db')
        cursor = connection.cursor()
        cursor.execute(query,
                       (self.unique_id, self.name, self.balance, self.login, self.password_hash, self.time_register))
        connection.commit()
        cursor.close()

    def update_balance(self):
        """Updates user's balance"""
        connection = sqlite3.connect('h.db')
        cursor = connection.cursor()
        cursor.execute("""
        UPDATE EntityUser
        SET (balance) = (?)
        WHERE unique_id = (?)
        """, (self.balance, self.unique_id))
        connection.commit()
        cursor.close()


def get_register_data(message: str) -> EntityUser:
    values = message.split('\n', 3)
    for value in values:
        if len(value) > 36 or len(value) == 0:
            raise Exception('Некорректные данные')

    name = values[0]
    login = values[1]
    pass1 = values[2]
    pass2 = values[3]

    if pass1 != pass2:
        raise Exception('Пароли не совпадают')

    user = EntityUser()
    user.name = name
    user.login = login
    user.balance = config_controller.get_value('default_balance')
    user.unique_id = uuid.uuid4().__str__()
    user.password_hash = hashlib.sha224(pass1.encode()).hexdigest()
    user.time_register = datetime.datetime.now()

    return user


def auth(login: str, password: str) -> EntityUser():
    """Tries to find a user with specified login and password hash in database and returns it if it exists."""
    password_hash = hashlib.sha224(password.encode()).hexdigest()
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    __create_table__()
    user_auth = cursor.execute(f"select * from EntityUser where login = ? and password_hash = ?", (login, password_hash)).fetchone()
    cursor.close()
    user = EntityUser()
    user.unique_id = user_auth[0]
    user.name = user_auth[1]
    user.balance = user_auth[2]
    user.login = user_auth[3]
    user.password_hash = user_auth[4]
    user.time_register = user_auth[5]
    user.is_admin = table_admins.is_admin(user.unique_id)

    return user


def __create_table__():
    print('Creating table EntityUser')
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    # cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EntityUser(
    unique_id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(36),
    balance INTEGER,
    login VARCHAR(36) UNIQUE,
    password_hash TEXT,
    time_register DATETIME)
    """)
    connection.commit()
    cursor.close()
    print('Created table EntityUser')

