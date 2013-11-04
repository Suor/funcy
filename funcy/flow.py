from datetime import datetime, timedelta
from functools import wraps
from itertools import imap

from .decorators import decorator


__all__ = ['ignore', 'silent', 'retry', 'fallback',
           'limit_error_rate', 'ErrorRateExceeded',
           'post_processing', 'collecting', 'joining']


### Error handling utilities

# Not using @decorator here for speed,
# since @ignore and @silent should be used for very simple and fast functions
def ignore(errors, default=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                return default
        return wrapper
    return decorator

silent = ignore(Exception) # Ignore all real exceptions


@decorator
def retry(call, tries, errors=Exception):
    for attempt in xrange(tries):
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


### Post processing decorators

@decorator
def post_processing(call, func):
    return func(call())

collecting = post_processing(list)

@decorator
def joining(call, sep):
    return sep.join(imap(sep.__class__, call()))
