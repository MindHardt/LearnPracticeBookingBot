import datetime
import sqlite3


class Favorite:
    """Отель, добавленный в избранное"""
    unique_id = str()
    user_id = str()
    url = str()


class FavoriteData:
    """Данные об избранном за 1 запрос"""
    favorite_id = str()
    price = int()
    time = datetime.datetime


def __create_tables__():
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Favorites(
    unique_id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    url TEXT,
    FOREIGN KEY (user_id) REFERENCES EntityUser(unique_id)
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS FavoriteData(
    favorite_id VARCHAR(36),
    price INTEGER,
    time DATETIME,
    FOREIGN KEY (favorite_id) REFERENCES Favorites(unique_id)
    )""")
    connection.commit()
    cursor.close()
