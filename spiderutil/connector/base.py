from abc import abstractmethod


class Database:
    def __init__(self, name: str, db_type):
        self.name = name
        self.type = db_type

    @abstractmethod
    def count(self):
        pass
