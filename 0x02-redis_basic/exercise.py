#!/usr/bin/env python3
"""
Redis -> writing strings to redis
"""
import redis
import uuid
from typing import Union


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


if __name__ == '__main__':
    cache = Cache()
