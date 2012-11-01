# -*- coding: utf-8 -*-
from __future__ import print_function

from datetime import datetime, timedelta
from functools import wraps


def log(print_func=print):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            arg_words = list(args) + ['%s=%s' % t for t in kwargs.items()]
            print_func('Call %s(%s)' % (func.__name__, ', '.join(map(str, arg_words))))
            result = func(*args, **kwargs)
            print_func('-> %s' % repr(result))
            return result
        return wrapper
    return decorator


def log_errors(print_func=print):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print_func('%s: %s in %s' % (e.__class__.__name__, e, func.__name__))
                raise
        return wrapper
    return decorator
