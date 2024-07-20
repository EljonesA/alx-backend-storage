#!/usr/bin/env python3
"""
Redis -> writing strings to redis
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    '''
    This class writes strings to Redis
    '''

    def __init__(self):
        ''' Initializing cache class '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''
        Store the input data in Redis with a random key and return the key.
        note: all keys in redis must be/are strings
        '''
        key = str(uuid.uuid4())  # generate random key
        self._redis.set(key, data)  # store input data in redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        '''
        Retrieve data from Redis & optionally convert it using given callable.
        '''
        data = self._redis.get(key)
        if data is None:  # conserve redis.get behavior if key not present
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        ''' Retrieve a string from Redis. '''
        data = self.get(key)
        if data is None or not isinstance(data, bytes):
            return None
        return data.decode('utf-8')

    def get_int(self, key: str) -> Optional[int]:
        ''' Retrieve an integer from Redis. '''
        data = self.get(key)
        if data is None:
            return None
        return int(data)


if __name__ == '__main__':
    cache = Cache()
