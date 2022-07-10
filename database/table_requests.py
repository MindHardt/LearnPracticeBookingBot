import datetime
import sqlite3
from database.entity_request import EntityRequest
from database.table_users import EntityUser

connection = sqlite3.connect('h.db')
cursor = connection.cursor()


def save(request: EntityRequest):
    """Adds this request to a database for history"""
    # TODO: save(request: EntityRequest)
    pass


def get_history_of(user: EntityUser) -> list:
    """Gets all the history of specified user"""
    # TODO: get_history_of(user: EntityUser)
    pass


def get_history_for(date_from: datetime.datetime, date_to: datetime.datetime) -> list:
    """Gets all the history of all users between 2 provided time points"""
    # TODO: get_history_for(date_from: datetime.datetime, date_to: datetime.datetime)
    pass


def __create_table__():
    cursor.execute("PRAGMA foreign_keys=on")
    cursor.execute("CREATE TABLE IF NOT EXISTS EntityRequest(unique_id VARCHAR(36) PRIMARY KEY, destination TEXT, date_arrive DATETIME, date_depart DATETIME, "
                   "date_request DATETIME,"
                   "FOREIGN KEY (user_id) REFERENCES EntityUser(unique_id))")
    connection.commit()
