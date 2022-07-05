import datetime
from enum import Enum
import geopy


class QueryBuilder:

    # REQUIRED dates of living
    date_from = datetime.date
    date_to = datetime.date
    # REQUIRED center pos, is recognized from query
    location = geopy.Location
    # OPTIONAL defaults to 10 km [float]
    distance = 10.0
    # OPTIONAL price range [float]
    price_from = 0.0
    price_to = None
    # OPTIONAL food type [FoodType]
    food_type = None

    def is_valid(self) -> bool:
        return self.date_from is datetime.date and self.date_to is datetime.date and self.date_from < self.date_to and self.location is geopy.Location


class FoodType(Enum):
    Breakfast = 0
    ThreeTimes = 1


