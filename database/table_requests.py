import datetime
import sqlite3
from database.table_users import EntityUser


class EntityRequest:
    unique_id = str  # VARCHAR(36)
    user_id = EntityUser.unique_id  # FOREIGN KEY
    destination = str  # TEXT
    date_arrive = datetime.date  # DATETIME
    date_depart = datetime.date  # DATETIME
    date_request = datetime.datetime  # DATETIME

    def save(self):
        """Adds this request to a database for history"""
        __create_table__()
        connection = sqlite3.connect('h.db')
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO EntityRequest VALUES(?,?,?,?,?,?)
            """, (self.unique_id, self.destination, self.date_arrive, self.date_arrive, self.date_depart,
                  self.user_id))
        connection.commit()
        cursor.close()


def get_history_of(user: EntityUser) -> list:
    """Gets all the history of specified user"""
    __create_table__()
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    found = cursor.execute("""
            SELECT * FROM EntityRequest WHERE user_id = ?
            """, (user.unique_id,)).fetchall()
    cursor.close()
    return found


def get_history_for(date_from: datetime.datetime, date_to: datetime.datetime) -> list:
    """Gets all the history of all users between 2 provided time points"""
    __create_table__()
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    found = cursor.execute("""
                SELECT * FROM EntityRequest WHERE date_request BETWEEN ? AND ?
                """, (date_from, date_to)).fetchall()
    cursor.close()
    return found


def __create_table__():
    connection = sqlite3.connect('h.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("CREATE TABLE IF NOT EXISTS EntityRequest("
                   "unique_id VARCHAR(36) PRIMARY KEY, "
                   "destination TEXT, "
                   "date_arrive DATETIME, "
                   "date_depart DATETIME, "
                   "date_request DATETIME,"
                   "FOREIGN KEY (user_id) REFERENCES EntityUser(unique_id))")
    connection.commit()
    cursor.close()
