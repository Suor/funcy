# -*- coding: utf-8 -*-
from __future__ import print_function

from .decorators import decorator


__all__ = ['tap', 'log_calls', 'print_calls', 'log_errors', 'print_errors']


def tap(x):
    print(x)
    return x


@decorator
def log_calls(call, print_func, errors=True):
    signature = signature_repr(call)
    try:
        print_func('Call %s' % signature)
        result = call()
        print_func('-> %s from %s' % (smart_repr(result), signature))
        return result
    except BaseException as e:
        if errors:
            print_func('-> raised %s: %s in %s' % (e.__class__.__name__, e, signature))
        raise

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

