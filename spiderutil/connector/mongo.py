import pymongo

from .base import Database
from ..exceptions import NullPrimarySearchKeyException


class MongoDB(Database):

    def __init__(self, collection: str,
                 host='localhost',
                 port=27017,
                 db='spider',
                 primary_search_key=None):
        super(MongoDB, self).__init__(collection, 'MongoDB')

        self.host = host
        self.port = port
        self.db = db

        client = pymongo.MongoClient(host=host, port=port)
        database = client[db]
        self.conn = database[collection]

        self.primary_search_key = primary_search_key

    def check_connection(self):
        client = pymongo.MongoClient(host=self.host, port=self.port,
                                     serverSelectionTimeoutMS=3000, connectTimeoutMS=3000)
        client.admin.command('ismaster')

    def insert(self, documents):
        if type(documents) is list:
            return self.conn.insert_many(documents)
        else:
            return self.conn.insert_one(documents)

    def remove(self, filter, all=False):
        if all:
            return self.conn.delete_many(filter=filter)
        else:
            return self.conn.delete_one(filter=filter)

    def update(self, filter, update, all=False):
        """
        :param filter:
        :param update: Update operations, check https://docs.mongodb.com/manual/reference/operator/update/#id1 for more.
        :param all:
        :return:
        """
        if all:
            return self.conn.update_many(filter=filter, update=update)
        else:
            return self.conn.update_one(filter=filter, update=update)

    def replace(self, filter, replacement, **kwargs):
        return self.conn.replace_one(filter=filter, replacement=replacement, **kwargs)

    def find(self, filter, *args, all=False, **kwargs):
        if all:
            return self.conn.find(filter, *args, **kwargs)
        else:
            return self.conn.find_one(filter=filter, *args, **kwargs)

    def all(self, exclude_id=False):
        """
        Return all documents in the collection.
        :return: a iterator of all documents
        """
        if exclude_id:
            return self.conn.find({}, {'_id': False})
        else:
            return self.conn.find()

    def count(self, filter=None, **kwargs):
        """
        Return the count of filtered documents in the collection.
        :param filter: a dict contains filters
        :param kwargs: other parameters pymongo supports
        :return:
        """
        if filter is None:
            return self.conn.count_documents(filter={}, **kwargs)
        else:
            return self.conn.count_documents(filter=filter, **kwargs)

    def drop(self):
        """
        Drop the collection.
        :return: None
        """
        self.conn.drop()

    def create_index(self, index):
        """
        :param index: [('key', pymongo.HASHED)]
        :return: Index Name
        """
        return self.conn.create_index(index)

    def set_primary_search_key(self, primary_search_key):
        self.primary_search_key = primary_search_key

    def add(self, item):
        if self.primary_search_key:
            self.insert({self.primary_search_key: item})
        else:
            raise NullPrimarySearchKeyException

    def __contains__(self, item):
        if self.primary_search_key:
            return self.count({self.primary_search_key: item}) > 0
        else:
            raise NullPrimarySearchKeyException()
