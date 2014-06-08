from datetime import datetime, timedelta
from collections import Hashable
import threading

from .cross import imap, xrange
from .decorators import decorator, wraps


__all__ = ['raiser', 'ignore', 'silent', 'retry', 'fallback',
           'limit_error_rate', 'ErrorRateExceeded',
           'post_processing', 'collecting', 'joining',
           'once', 'once_per']


### Error handling utilities

def raiser(exception_or_class=Exception, *args, **kwargs):
    def _raiser(*a, **kw):
        if args or kwargs:
            raise exception_or_class(*args, **kwargs)
        else:
            raise exception_or_class
    return _raiser


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


### Initialization helpers

def once_per(*argnames):
    def once(func):
        lock = threading.Lock()
        done_set = set()
        done_list = list()

        func_argnames = func.__code__.co_varnames[:func.__code__.co_argcount]
        def get_arg(name, args, kwargs):
            if name in kwargs:
                return kwargs[name]
            elif name in func_argnames:
                return args[func_argnames.index(name)]
            else:
                raise TypeError("%s() doesn't have argument named %s" % (func.__name__, name))

        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                values = tuple(get_arg(name, args, kwargs) for name in argnames)
                if isinstance(values, Hashable):
                    done, add = done_set, done_set.add
                else:
                    done, add = done_list, done_list.append

                if values not in done:
                    add(values)
                    return func(*args, **kwargs)
        return wrapper
    return once

once = once_per()
