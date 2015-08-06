from datetime import datetime, timedelta
from collections import Hashable
import time
import threading

from .cross import imap, xrange
from .decorators import decorator, wraps, get_argnames, arggetter


__all__ = ['raiser', 'ignore', 'silent', 'suppress', 'retry', 'fallback',
           'limit_error_rate', 'ErrorRateExceeded',
           'post_processing', 'collecting', 'joining',
           'once', 'once_per', 'once_per_args']


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


### Backport of Python 3.4 suppress
try:
    from contextlib import suppress
except ImportError:
    class suppress(object):
        """Context manager to suppress specified exceptions

        After the exception is suppressed, execution proceeds with the next
        statement following the with statement.
        """

        def __init__(self, *exceptions):
            self._exceptions = exceptions

        def __enter__(self):
            pass

        def __exit__(self, exctype, excinst, exctb):
            # Unlike isinstance and issubclass, CPython exception handling
            # currently only looks at the concrete type hierarchy (ignoring
            # the instance and subclass checking hooks). While Guido considers
            # that a bug rather than a feature, it's a fairly hard one to fix
            # due to various internal implementation details. suppress provides
            # the simpler issubclass based semantics, rather than trying to
            # exactly reproduce the limitations of the CPython interpreter.
            #
            # See http://bugs.python.org/issue12029 for more details
            return exctype is not None and issubclass(exctype, self._exceptions)


@decorator
def retry(call, tries, errors=Exception, timeout=0):
    if isinstance(errors, list):
        # because `except` does not catch exceptions from list
        errors = tuple(errors)

    for attempt in xrange(tries):
        try:
            return call()
        except errors:
            # Reraise error on last attempt
            if attempt + 1 == tries:
                raise
            else:
                timeout_value = timeout(attempt) if callable(timeout) else timeout
                if timeout_value > 0:
                    time.sleep(timeout_value)


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

        get_arg = arggetter(func)

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

def once_per_args(func):
    return once_per(*get_argnames(func))(func)
