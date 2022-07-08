from database.entity_user import EntityUser
import sqlite3


def auth(login: str, password_hash: str) -> EntityUser():
    """Tries to find a user with specified login and password hash in database and returns it if it exists."""
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

    return user


def try_register(user: EntityUser()):
    """Tries to register user with specified data."""
    __create_table__()
    query = "insert into 'EntityUser'(unique_id, name, balance, login, password_hash) values(?,?,?,?,?);"
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    cursor.execute(query, (user.unique_id, user.name, user.balance, user.login, user.password_hash))
    connection.commit()
    cursor.close()


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
    password_hash TEXT)
    """)
    connection.commit()
    cursor.close()
    print('Created table EntityUser')
