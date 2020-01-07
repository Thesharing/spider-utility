import pymongo

from .base import Database
from ..exceptions import NullPrimarySearchKeyException


class MongoDB(Database):
    """
    Simplified MongoDB Connector based on `PyMongo <https://github.com/mongodb/mongo-python-driver>`_.

    """

    def __init__(self, collection: str,
                 host='localhost',
                 port=27017,
                 db='spider',
                 primary_key=None):
        """
        :param collection: name of collection
        :param host: host address of MongoDB, default is ``localhost``
        :param port: port of MongoDB, default is ``27017``
        :param db: name of database, default is ``spider``
        :param primary_key: primary key used by ``in`` and ``add``
        """
        super(MongoDB, self).__init__(collection, 'MongoDB')

        self.host = host
        self.port = port
        self.db = db

        client = pymongo.MongoClient(host=host, port=port)
        database = client[db]

        #: The PyMongo instance
        self.conn = database[collection]

        self.primary_key = primary_key

    def check_connection(self):
        """
        Check whether the MongoDB service is running or not. If not running, this will raise ``pymongo.errors.ServerSelectionTimeoutError``.

          mongo.check_connection()

        """
        client = pymongo.MongoClient(host=self.host, port=self.port,
                                     serverSelectionTimeoutMS=3000,
                                     connectTimeoutMS=3000)
        client.admin.command('ismaster')

    def insert(self, documents):
        """
        Insert document(s). ::

          mongo.insert({'key': 'value'})

        :param documents: dict, or a list of dict
        :return: `pymongo.results.InsertOneResult` or `pymongo.results.InsertManyResult`
        """
        if type(documents) is list:
            return self.conn.insert_many(documents)
        else:
            return self.conn.insert_one(documents)

    def remove(self, filter, all=False, **kwargs):
        """
        Remove filtered document(s).

        :param filter: a dict that specifies delete criteria using `query operators <https://docs.mongodb.com/manual/reference/operator/>`_ like: ``{'fieldName': 'value'}``
        :param all: delete all filtered documents or just one, default is ``False``
        :param kwargs: other params, see `db.collection.deleteOne() <https://docs.mongodb.com/manual/reference/method/db.collection.deleteOne/>`_ for more
        :return: `pymongo.results.DeleteResult`
        """
        if all:
            return self.conn.delete_many(filter=filter, **kwargs)
        else:
            return self.conn.delete_one(filter=filter, **kwargs)

    delete = remove

    def update(self, filter, update, all=False, **kwargs):
        """
        Modifies an existing document or documents in a collection. The method can modify specific fields of an existing document or documents or replace an existing document entirely, depending on the update operator expressions.

        :param filter: a dict that specifies update criteria using `query operators <https://docs.mongodb.com/manual/reference/operator/>`_
        :param update: a document contains `update operator expressions <https://docs.mongodb.com/manual/reference/operator/update/>`_
        :param all: update single document or all the documents that match the specified filter, default is ``False``
        :param kwargs: other params, see `db.collection.updateOne() <https://docs.mongodb.com/manual/reference/method/db.collection.updateOne/>`_ for more
        :return: ``pymongo.results.UpdateResult``
        """
        if all:
            return self.conn.update_many(filter=filter, update=update, **kwargs)
        else:
            return self.conn.update_one(filter=filter, update=update, **kwargs)

    def replace(self, filter, replacement, **kwargs):
        """
        Replaces a single document within the collection based on the filter.

        :param filter: a dict that specifies update criteria using `query operators <https://docs.mongodb.com/manual/reference/operator/>`_ like: ``{'fieldName': 'value'}``
        :param replacement: The replacement document. Cannot contain update operators.
        :param kwargs: other params, see `db.collection.replaceOne() <https://docs.mongodb.com/manual/reference/method/db.collection.replaceOne/>`_ for more
        :return: ``pymongo.results.UpdateResult``
        """
        return self.conn.replace_one(filter=filter, replacement=replacement,
                                     **kwargs)

    def find(self, filter, *args, all=False, exclude_id=False, **kwargs):
        """
        Selects documents in a collection or view and returns a cursor to the selected documents.

        :param filter: optional, a dict that specifies query selection criteria using `query operators <https://docs.mongodb.com/manual/reference/operator/>`_ like: ``{'fieldName': 'value'}``
        :param args: optional, contains projection that specifies the fields to return using `projection operators <https://docs.mongodb.com/manual/reference/operator/projection/>`_ , omit this parameter to return all fields in the matching document
        :param all: return all matching documents or just single one, default is ``False``
        :param exclude_id: exclude ``_id`` field in results or not, default is ``False``
        :param kwargs: other params, see `db.collection.findOne() <https://docs.mongodb.com/manual/reference/method/db.collection.findOne/>`_
        :return: if ``all``, returns a cursor to the documents that match the query criteria; else returns only one document that satisfies the criteria
        """

        if exclude_id and {'_id': False} not in args:
            args += ({'_id': False},)
        if all:
            return self.conn.find(filter, *args, **kwargs)
        else:
            return self.conn.find_one(filter, *args, **kwargs)

    def all(self, exclude_id=False):
        """
        Return all documents in the collection.

        :param exclude_id: exclude ``_id`` field in results or not, default is ``False``
        :return: a generator of all documents
        """
        if exclude_id:
            return self.conn.find({}, {'_id': False})
        else:
            return self.conn.find()

    def count(self, filter=None, **kwargs):
        """
        Return the count of filtered documents in the collection. ::

          db.count({'grade', {'$gt': 90}})

        :param filter: a dict contains filters
        :param kwargs: other parameters PyMongo supports, see `official doc <https://docs.mongodb.com/manual/reference/method/db.collection.countDocuments/>`_ for more
        :return: the count
        """
        if filter is None:
            return self.conn.count_documents(filter={}, **kwargs)
        else:
            return self.conn.count_documents(filter=filter, **kwargs)

    def drop(self):
        """
        Drop the collection. ::

            mongo.drop()

        :return: None
        """
        self.conn.drop()

    def create_index(self, index, **kwargs):
        """
        Creates indexes on collections.

        To create a single key ascending index on the key ``'mike'`` we just
        use a string argument::

          mongo.create_index("mike")

        For a compound index on ``'mike'`` descending and ``'eliot'``
        ascending we need to use a list of tuples::

          mongo.create_index([("mike", MongoDB.DESCENDING),
                              ("eliot", MongoDB.ASCENDING)])

        :param index: ``str``, or ``list`` of ``tuple`` that contains index key and index type
        :return: ``str``, index name
        """
        return self.conn.create_index(index, **kwargs)

    def set_primary_key(self, primary_key):
        """
        Set the primary search key. The primary search key is not a concept in MongoDB. This key is used for `add` and `in` operations.

        For example, the primary search key can be set at the init::

          mongo = Mongo('students', primary_key='id')

        or explicitly set afterwards::

          mongo = Mongo('students')
          mongo.set_primary_key('id')

        Then used as::

          if 'mike' not in mongo:
            mongo.add('mike')

        This trick is used to simplify simple operations.

        :param primary_key: str, the name of primary key
        :return: None
        """
        self.primary_key = primary_key

    def add(self, item):
        """
        Different from ````

        :param item:
        :return:
        """
        if self.primary_key:
            self.insert({self.primary_key: item})
        else:
            raise NullPrimarySearchKeyException()

    def __contains__(self, item):
        if self.primary_key:
            return self.count({self.primary_key: item}) > 0
        else:
            raise NullPrimarySearchKeyException()


class Index:
    """
    `Index Types <https://docs.mongodb.com/manual/indexes/index.html>`_
    """

    ASCENDING = 1
    """Ascending sort order."""
    DESCENDING = -1
    """Descending sort order."""
    GEO2D = "2d"
    """Index specifier for a 2-dimensional `geospatial index <http://docs.mongodb.org/manual/core/2d/>`_."""
    GEOHAYSTACK = "geoHaystack"
    """Index specifier for a 2-dimensional `haystack index <http://docs.mongodb.org/manual/core/geohaystack/>`_."""
    GEOSPHERE = "2dsphere"
    """Index specifier for a `spherical geospatial index <http://docs.mongodb.org/manual/core/2dsphere/>`_."""
    HASHED = "hashed"
    """Index specifier for a `hashed index <http://docs.mongodb.org/manual/core/index-hashed/>`_."""
    TEXT = "text"
    """Index specifier for a `text index <http://docs.mongodb.org/manual/core/index-text/>`_."""


class Query:
    """
    `Query Operators <https://docs.mongodb.com/manual/reference/operator/query/#query-selectors>`_
    """

    EQUAL = '$eq'
    """`$eq <https://docs.mongodb.com/manual/reference/operator/query/eq/#op._S_eq>`_ : Matches values that are equal to a specified value."""
    GREATER = '$gt'
    """`$gt <https://docs.mongodb.com/manual/reference/operator/query/gt/#op._S_gt>`_ :  Matches values that are greater than a specified value."""
    GREATER_AND_EQUAL = '$gte'
    """`$gte <https://docs.mongodb.com/manual/reference/operator/query/gte/#op._S_gte>`_ : Matches values that are greater than or equal to a specified value."""
    IN = '$in'
    """`$in <https://docs.mongodb.com/manual/reference/operator/query/in/#op._S_in>`_ : Matches any of the values specified in an array."""
    LESS = '$lt'
    """`$lt <https://docs.mongodb.com/manual/reference/operator/query/lt/#op._S_lt>`_ : Matches values that are less than a specified value."""
    LESS_AND_EQUAL = '$lte'
    """`$lte <https://docs.mongodb.com/manual/reference/operator/query/lte/#op._S_lte>`_ : Matches values that are less than or equal to a specified value."""
    NOT_EQUAL = '$ne'
    """`$ne <https://docs.mongodb.com/manual/reference/operator/query/ne/#op._S_ne>`_ : Matches all values that are not equal to a specified value."""
    NOT_IN = '$nin'
    """`$nin <https://docs.mongodb.com/manual/reference/operator/query/nin/#op._S_nin>`_ : Matches none of the values specified in an array."""

    AND = '$and'
    """`$and <https://docs.mongodb.com/manual/reference/operator/query/and/#op._S_and>`_ : Joins query clauses with a logical **AND** returns all documents that match the conditions of both clauses."""
    NOT = '$not'
    """`$not <https://docs.mongodb.com/manual/reference/operator/query/not/#op._S_not>`_ : 	Inverts the effect of a query expression and returns documents that do not match the query expression."""
    NOR = '$nor'
    """`$nor <https://docs.mongodb.com/manual/reference/operator/query/nor/#op._S_nor>`_ : Joins query clauses with a logical **NOR** returns all documents that fail to match both clauses."""
    OR = '$or'
    """`$or <https://docs.mongodb.com/manual/reference/operator/query/or/#op._S_or>`_ : Joins query clauses with a logical **OR** returns all documents that match the conditions of either clause."""
    EXISTS = '$exists'
    """`$exists <https://docs.mongodb.com/manual/reference/operator/query/exists/#op._S_exists>`_ : Matches documents that have the specified field."""
    TYPE = '$type'
    """`$type <https://docs.mongodb.com/manual/reference/operator/query/type/#op._S_type>`_ : 	Selects documents if a field is of the specified type."""
    EXPR = '$expr'
    """`$expr <>`"""