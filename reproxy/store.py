# -*- coding: utf-8 -*-

from redis import StrictRedis
import pickle

import settings


class PickledRedis(StrictRedis):

    def pickle_get(self, name):
        pickled_value = super(PickledRedis, self).get(name)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)

    def pickle_set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return super(PickledRedis, self).set(
            name, pickle.dumps(value),
            ex, px, nx, xx
        )


class RedisQueue(object):
    def __init__(self, _r, name, namespace='queue'):
        self.__db = _r
        self.key = '%s:%s' % (namespace, name)

    def size(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.size() == 0

    def put(self, item):
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        return item

    def get_nowait(self):
        return self.get(False)

    def clear(self):
        self.__db.delete(self.key)


r = PickledRedis(
    socket_timeout=0.5,  # seconds, see `socket.settimeout()`
    retry_on_timeout=True,
    **settings.REDIS_CONF
)
