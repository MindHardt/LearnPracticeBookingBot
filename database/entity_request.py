import datetime

from database.entity_user import EntityUser


class EntityRequest:
    user_id = EntityUser.unique_id  # FOREIGN KEY
    location_lon = float  # NUMERIC(10)
    location_lat = float  # NUMERIC(10)
    date_arrive = datetime.date  # DATETIME
    date_depart = datetime.date  # DATETIME
    date_request = datetime.datetime  # DATETIME
    optional_filters = []  # TEXT
    
     def __create_table__():
        cursor.execute("PRAGMA foreign_keys=on")
        cursor.execute("CREATE TABLE IF NOT EXISTS EntityRequest(location_lon NUMERIC(10), "
                       "location_lat NUMERIC(10), date_arrive DATETIME, date_depart DATETIME, "
                       "date_request DATETIME, optional_filters TEXT,"
                       "FOREIGN KEY (user_id) REFERENCES EntityUser(unique_id))")
        connection.commit()
