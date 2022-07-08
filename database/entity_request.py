import datetime

from database.entity_user import EntityUser


class EntityRequest:
    unique_id = str  # VARCHAR(36)
    user_id = EntityUser.unique_id  # FOREIGN KEY
    destination = str  # TEXT
    date_arrive = datetime.date  # DATETIME
    date_depart = datetime.date  # DATETIME
    date_request = datetime.datetime  # DATETIME

