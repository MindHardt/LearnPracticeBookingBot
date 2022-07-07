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

