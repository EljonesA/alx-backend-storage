#!/usr/bin/env python3
"""
Web caching and counting with Redis
"""
import redis
import requests
from typing import Callable
import functools

# Initialize Redis client
r = redis.Redis()


def cache_result(ttl: int):
    """Decorator to cache the result of a function for a given TTL."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(url: str) -> str:
            cached_result = r.get(f"cache:{url}")
            if cached_result:
                return cached_result.decode('utf-8')
            result = func(url)
            r.setex(f"cache:{url}", ttl, result)
            return result
        return wrapper
    return decorator


def count_requests(func: Callable) -> Callable:
    """Decorator to count the number of requests to a URL."""
    @functools.wraps(func)
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")
        return func(url)
    return wrapper


@cache_result(ttl=10)
@count_requests
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and return it."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"

    print(get_page(url))
    print(get_page(url))
    print(f"Access count for {url}: {r.get(f'count:{url}').decode('utf-8')}")
