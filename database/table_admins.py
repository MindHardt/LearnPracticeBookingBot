import sqlite3


def add_admin(user_id: str):
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    cursor.execute("insert into admins(id_admin) values(?)", (user_id,))
    connection.commit()
    cursor.close()
    return


def revoke_admin(user_id: str):
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    cursor.execute(f"delete from Admins where id_admin = ?", (user_id,))
    connection.commit()
    cursor.close()
    return


def is_admin(user_id: str) -> bool:
    __create_table__()
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    admin_id = cursor.execute(f"select id_admin from Admins where id_admin = ?", (user_id,)).fetchone()
    cursor.close()
    return admin_id is not None


def __create_table__():
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Admins(
    id_admin VARCHAR(36) UNIQUE,
    FOREIGN KEY (id_admin) REFERENCES EntityUser(unique_id))""")
    connection.commit()
    cursor.close()
    return
