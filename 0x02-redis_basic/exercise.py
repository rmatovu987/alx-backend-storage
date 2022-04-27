#!/usr/bin/env python3
"""Create a Cache class. In the __init__ method,
store an instance of the Redis client as a private variable named
_redis (using redis.Redis()) and flush the instance using flushdb. """
import uuid
from functools import wraps
from typing import Union, Optional, Callable

import redis


def call_history(method: Callable) -> Callable:
    """ memorize user actions"""
    method_key = method.__qualname__
    inputs = method_key + ':inputs'
    outputs = method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ function  wrapped """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable):
    """ display the history call """
    method_key = method.__qualname__
    inputs = method_key + ":inputs"
    outputs = method_key + ":outputs"
    redis = method.__self__._redis
    count = redis.get(method_key).decode("utf-8")
    print("{} was called {} times:".format(method_key, count))
    ListInput = redis.lrange(inputs, 0, -1)
    ListOutput = redis.lrange(outputs, 0, -1)
    allData = list(zip(ListInput, ListOutput))
    for key, data in allData:
        attr, data = key.decode("utf-8"), data.decode("utf-8")
        print("{}(*{}) -> {}".format(method_key, attr, data))


def count_calls(method: Callable) -> Callable:
    """Counts method calls"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapped function"""
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """A redis cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that takes a data argument and returns a string"""
        random_key = str(uuid.uuid1())
        self._redis.mset({random_key: data})
        return random_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Take a key and return the type"""
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, data: str) -> str:
        """Convert the bytes to str"""
        return self._redis.get(data).decode('utf-8')

    def get_int(self, data: str) -> int:
        """Convert bytes to int"""
        return int(self._redis.get(data))
