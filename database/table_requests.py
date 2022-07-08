import datetime

from database.entity_request import EntityRequest
from database.entity_user import EntityUser


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
