from abc import abstractmethod


class Database:
    """
    *Abstract class*.

    The base class of all database connector.
    """
    def __init__(self, name: str, db_type):
        """
        :param name: name of the target database
        :param db_type: name of connector type
        """
        self.name = name
        self.type = db_type

    @abstractmethod
    def count(self):
        """
        :return: The count of target database.
        """
        raise NotImplementedError

    @abstractmethod
    def add(self, item):
        """
        Add an item.

        :param item: target item(s)
        :return: ``Boolean`` (success or not) or ``None``.
        """
        raise NotImplementedError
