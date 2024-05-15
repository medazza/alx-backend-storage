#!/usr/bin/env python3
"""
    0. Writing strings to Redis
    1. Reading from Redis and recovering original type
    2. Incrementing values
    3. Storing lists
    4. Retrieving lists
"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def replay(method: Callable) -> None:
    """function to display the history of calls of a particular func"""
    r = method.__self__._redis
    qualname = method.__qualname__
    inputs_key = f"{qualname}:inputs"
    outputs_key = f"{qualname}:outputs"

    inputs = r.lrange(inputs_key, 0, -1)
    outputs = r.lrange(outputs_key, 0, -1)

    num_calls = r.get(qualname)
    if num_calls:
        num_calls = num_calls.decode('utf-8')
    else:
        num_calls = '0'

    print(f"{qualname} was called {num_calls} times:")

    for inp, out in zip(inputs, outputs):
        print(
            "{}(*{}) -> {}".format(
                qualname, inp.decode("utf-8"), out.decode("utf-8")
            )
        )


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a particular function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper"""
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))

        return result
    return wrapper


class Cache:
    """Cache class"""
    def __init__(self) -> None:
        """store an instance of the Redis client as
            a private variable named _redis
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key, store the input data in Redis
            using the random key and return the key
        """
        keyx = str(uuid.uuid4())
        if isinstance(data, (int, float)):
            data = str(data)
        self._redis.set(name=keyx, value=data)
        return keyx

    def get(self, key: str, fn: Optional[Callable] =
            None) -> Union[str, bytes, int, float]:
        """method that take a key string argument and an optional Callable"""
        val = self._redis.get(name=key)
        if val is None:
            return val
        if fn:
            return fn(val)
        return val

    def get_str(self, key: str) -> Optional[str]:
        """Get from redis"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Get from redis"""
        val = self.get(key)
        return int(val) if val else None
