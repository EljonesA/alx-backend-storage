#!/usr/bin/env python3
"""
Redis -> writing strings to redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    ''' Decorator to count calls to the method using Redis INCR. '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        ''' Increment the call count and call the original method.'''
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """Store input arguments and output in Redis."""
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"

        # store input arguments
        self._redis.rpush(key_inputs, str(args))

        # call original method & store its output
        result = method(self, *args, **kwargs)
        self._redis.rpush(key_outputs, str(result))
        return result
    return wrapper


def replay(method: Callable):
    """ Display the history of calls of a particular function. """
    key_inputs = f"{method.__qualname__}:inputs"
    key_outputs = f"{method.__qualname__}:outputs"
    redis_instance = method.__self__._redis

    inputs = redis_instance.lrange(key_inputs, 0, -1)
    outputs = redis_instance.lrange(key_outputs, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    '''
    This class writes strings to Redis
    '''

    def __init__(self):
        ''' Initializing cache class '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
