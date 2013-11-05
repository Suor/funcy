# -*- coding: utf-8 -*-
from __future__ import print_function

from .decorators import decorator


__all__ = ['tap', 'log_calls', 'print_calls', 'log_errors', 'print_errors']


def tap(x):
    print(x)
    return x


# TODO:
#   - log exceptions
#   - verbose return line (call func_name(args) returns ...)
#   - better args/kwargs stringification
@decorator
def log_calls(call, print_func):
    arg_words = list(call._args) + ['%s=%s' % t for t in call._kwargs.items()]
    print_func('Call %s(%s)' % (call._func.__name__, ', '.join(map(str, arg_words))))
    result = call()
    print_func('-> %s' % repr(result))
    return result

print_calls = log_calls(print)


@decorator
def log_errors(call, print_func):
    try:
        return call()
    except Exception as e:
        print_func('%s: %s in %s' % (e.__class__.__name__, e, call._func.__name__))
        raise

print_errors = log_errors(print)
