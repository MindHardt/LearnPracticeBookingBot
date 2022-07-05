import datetime
import geopy


class QueryBuilder:

    # REQUIRED dates of living
    date_from = datetime.date
    date_to = datetime.date
    # REQUIRED center pos, is recognized from query
    location = geopy.Location
    # OPTIONAL defaults to 10 km
    distance = float
    # OPTIONAL price range
    price_from = float
    price_to = float

    def __init__(self, date_from, date_to, location):
        self.date_from = date_from
        self.date_to = date_to
        self.location = location

    def is_valid(self) -> bool:
        return self.date_from is datetime.date and self.date_to is datetime.date and self.date_from < self.date_to and self.location is geopy.Location



