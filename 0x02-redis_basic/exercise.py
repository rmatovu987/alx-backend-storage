#!/usr/bin/env python3
"""Create a Cache class. In the __init__ method, store an instance of the Redis client as a private variable named
_redis (using redis.Redis()) and flush the instance using flushdb. """
import uuid
from typing import Union, Optional, Callable

import redis


class Cache:
    """A redis cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that takes a data argument and returns a string"""
        random_key = str(uuid.uuid1())
        self._redis.mset({random_key: data})
        return random_key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
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
