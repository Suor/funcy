# -*- coding: utf-8 -*-
from __future__ import print_function

from .decorators import decorator


__all__ = ['tap', 'log_calls', 'print_calls', 'log_errors', 'print_errors']


def tap(x):
    print(x)
    return x


# TODO: log exceptions
@decorator
def log_calls(call, print_func):
    arg_words = list(call._args) + ['%s=%s' % t for t in call._kwargs.items()]
    print_func('Call %s(%s)' % (call._func.__name__, ', '.join(map(str, arg_words))))
    result = call()
    print_func('-> %s from %s' % (smart_repr(result), signature))
    return result

print_calls = log_calls(print)


@decorator
def log_errors(call, print_func):
    try:
        return call()
    except Exception as e:
        print_func('%s: %s in %s' % (e.__class__.__name__, e, signature_repr(call)))
        raise

print_errors = log_errors(print)


def signature_repr(call):
    args_repr = map(smart_repr, call._args)
    kwargs_repr = ['%s=%s' % (key, smart_repr(value)) for key, value in call._kwargs.items()]
    return '%s(%s)' % (call._func.__name__, ', '.join(args_repr + kwargs_repr))

def smart_repr(value):
    if isinstance(value, (str, unicode)):
        return repr(value)
    else:
        return str(value)

