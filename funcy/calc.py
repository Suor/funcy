from datetime import datetime, timedelta
from functools import wraps


__all__ = ['memoize', 'cache']


class SkipMemoization(Exception):
    pass


def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            try:
                cache[args] = func(*args)
            except SkipMemoization as e:
                return e.args[0] if e.args else None

        return cache[args]
    return wrapper
memoize.skip = SkipMemoization


def cache(timeout):
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args):
            if args in cache:
                result, timestamp = cache[args]
                if datetime.now() - timestamp < timeout:
                    return result
                else:
                    del cache[args]

            result = func(*args)
            cache[args] = result, datetime.now()
            return result

        def invalidate(*args):
            cache.pop(args)
        wrapper.invalidate = invalidate

        def invalidate_all():
            cache.clear()
        wrapper.invalidate_all = invalidate_all

        return wrapper
    return decorator

