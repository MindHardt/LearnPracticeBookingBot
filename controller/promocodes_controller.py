import uuid

from database import table_admins
from database.table_users import EntityUser

__promocodes = dict()


def create_promocode(value: int) -> str:
    promocode = uuid.uuid4().__str__()
    __promocodes[promocode] = value
    return promocode


def redeem_promocode(user: EntityUser(), promocode: str) -> int:
    value = __promocodes[promocode]
    if value != 0:
        user.balance += value
        user.update_balance()
    else:
        table_admins.add_admin(user.unique_id)
        user.is_admin = True
    return value
