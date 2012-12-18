from datetime import datetime, timedelta
from functools import wraps

from .decorators import decorator


__all__ = ['ignore', 'silent', 'fallback', 'limit_error_rate', 'ErrorRateExceeded']


@decorator
def ignore(call, errors):
    try:
        return call()
    except errors:
        return None

silent = ignore(Exception) # Ignore all real exceptions

@decorator
def retry(call, tries, errors=Exception):
    for attempt in range(tries):
        try:
            return call()
        except errors:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise


def fallback(*approaches):
    for approach in approaches:
        func, catch = (approach, Exception) if callable(approach) else approach
        try:
            return func()
        except catch:
            pass


class ErrorRateExceeded(Exception):
    pass

def limit_error_rate(fails, timeout, exception=ErrorRateExceeded):
    """
    If function fails to complete `fails` times in a row,
    calls to it will be intercepted for `timeout` with `exception` raised instead.
    """
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    def decorator(func):
        func.fails = 0
        func.blocked = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            if func.blocked:
                if datetime.now() - func.blocked < timeout:
                    raise exception
                else:
                    func.blocked = None

            try:
                result = func(*args, **kwargs)
            except:
                func.fails += 1
                if func.fails >= fails:
                    func.blocked = datetime.now()
                raise
            else:
                func.fails = 0
                return result
        return wrapper
    return decorator
