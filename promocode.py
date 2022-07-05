import uuid


class Promocode(object):

    name = str
    value = int
    is_disposed = bool

    def __init__(self, value):
        self.name = uuid.uuid4().__str__()
        self.value = value
        self.is_disposed = False

    def dispose(self):
        self.is_disposed = True
        