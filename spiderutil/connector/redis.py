from abc import abstractmethod

import redis

from .base import Database


class Redis(Database):
    def __init__(self, name: str,
                 host='localhost',
                 port=6379):
        super(Redis, self).__init__(name, 'Redis')
        self.host = host
        self.port = port

        self.conn = redis.StrictRedis(host=host,
                                      port=port,
                                      decode_responses=True)

    def check_connection(self):
        conn = redis.StrictRedis(host=self.host, port=self.port,
                                 decode_responses=True)
        conn.client_list()

    @abstractmethod
    def count(self):
        pass


class RedisSet(Redis):

    def add(self, values):
        return self.conn.sadd(self.name, values)

    def count(self):
        return self.conn.scard(self.name)

    def empty(self):
        return self.conn.scard(self.name) <= 0

    def pop(self):
        return self.conn.spop(self.name)

    def remove(self, values):
        return self.conn.srem(self.name, values)

    def rand(self, number=None):
        if number:
            return self.conn.srandmember(self.name, number)
        else:
            return self.conn.srandmember(self.name)

    def is_member(self, value):
        return self.conn.sismember(self.name, value)

    def all(self):
        return self.conn.smembers(self.name)

    def flush_all(self):
        return self.conn.delete(self.name)


class RedisHash(Redis):

    def add(self, key):
        return self.conn.hsetnx(self.name, key, 0)

    def count(self):
        return self.conn.hlen(self.name)

    def empty(self):
        return self.conn.hlen(self.name) <= 0

    def remove(self, keys):
        return self.conn.hdel(self.name, keys)

    def exists(self, key):
        return self.conn.hexists(self.name, key)

    def all(self):
        return self.conn.hgetall(self.name)

    def get(self, keys):
        """
        :param keys: a single key or a list of keys
        :return: a string, or a list of string correspondingly
        """
        if type(keys) is list:
            return self.conn.hmget(self.name, keys)
        else:
            return self.conn.hget(self.name, keys)

    def set(self, mapping: dict):
        if len(mapping) > 1:
            return self.conn.hmset(self.name, mapping)
        elif len(mapping) == 1:
            (key, value), = mapping.items()
            return self.conn.hset(self.name, key, value)

    def increment(self, key, value: int = 1):
        return self.conn.hincrby(self.name, key, value)
