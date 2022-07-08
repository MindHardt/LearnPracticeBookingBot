from database.entity_user import EntityUser
import sqlite3

connection = sqlite3.connect('h.db')
cursor = connection.cursor()


def auth(login: str, password_hash: int) -> EntityUser():
    """Tries to find a user with specified login and password hash in database and returns it if it exists."""
    # TODO: auth(login: str, password_hash: int)
    login = #задается
    password_hash = #задается
    user_auth = [x for x in cursor.execute(f"select * from EntityUser where login = {login} and password_hash = {password_hash}").fetchall()]
    for x in user_auth:
        unique_id = x[0]
        name = x[1]
        balance = x[2]
        login = x[3]
        password_hash = x[4]
    pass


def try_register(user: EntityUser()) -> bool:
    """Tries to register user with specified data and returns True if succeeds and False otherwise. It may fail due to repeating login."""
    # TODO: try_register(user: EntityUser)
    login = #задается
    users_login = [x[0] for x in cursor.execute(f"select login from EntityUser").fetchall()]
    if login in users_login:
        return len(users_login) > 0
        pass
    else:
        sql = ("insert into 'EntityUser'(unique_id, name, balance, login, password_hash) values(?,?,?,?);")
        cursor.execute(sql, (unique_id, name, balance, login, password_hash))
        connection.commit()
    pass


def __create_table__():
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("CREATE TABLE IF NOT EXISTS EntityUser(unique_id VARCHAR(36) PRIMARY KEY, "
                       "name VARCHAR(36), balance INTEGER, login VARCHAR(36) UNIQUE, "
                       "password_hash INTEGER")
    connection.commit()
