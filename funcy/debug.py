# -*- coding: utf-8 -*-
from __future__ import print_function

from .decorators import decorator


__all__ = ['log', 'log_errors']


@decorator
def log(call, print_func=print):
    arg_words = list(call.args) + ['%s=%s' % t for t in call.kwargs.items()]
    print_func('Call %s(%s)' % (call.func.__name__, ', '.join(map(str, arg_words))))
    result = call()
    print_func('-> %s' % repr(result))
    return result


@decorator
def log_errors(call, print_func=print):
    try:
        return call()
    except Exception as e:
        print_func('%s: %s in %s' % (e.__class__.__name__, e, call.func.__name__))
        raise
