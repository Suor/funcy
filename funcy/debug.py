# -*- coding: utf-8 -*-
from __future__ import print_function
import re
import time
import traceback
from itertools import chain

from .cross import imap, basestring
from .decorators import decorator


__all__ = ['tap',
           'log_calls', 'print_calls',
           'log_enters', 'print_enters',
           'log_exits', 'print_exits',
           'log_errors', 'print_errors',
           'log_durations', 'print_durations']


def tap(x, label=None):
    if label:
        print('%s: %s' % (label, x))
    else:
        print(x)
    return x


@decorator
def log_calls(call, print_func, errors=True, stack=True):
    signature = signature_repr(call)
    try:
        print_func('Call %s' % signature)
        result = call()
        print_func('-> %s from %s' % (smart_repr(result), signature))
        return result
    except BaseException as e:
        if errors:
            print_func('-> ' + _format_error(call, e, stack))
        raise

print_calls = log_calls(print)


@decorator
def log_enters(call, print_func):
    print_func('Call %s' % signature_repr(call))
    return call()

print_enters = log_enters(print)


@decorator
def log_exits(call, print_func, errors=True, stack=True):
    try:
        result = call()
        print_func('-> %s from %s' % (smart_repr(result), signature_repr(call)))
        return result
    except BaseException as e:
        if errors:
            print_func('-> ' + _format_error(call, e, stack))
        raise

print_exits = log_exits(print)


@decorator
def log_errors(call, print_func, stack=True):
    try:
        return call()
    except Exception as e:
        print_func(_format_error(call, e, stack))
        raise

print_errors = log_errors(print)


def _format_error(call, e, stack=True):
    if stack:
        return traceback.format_exc() + '    raised in ' + signature_repr(call)
    else:
        return '%s: %s raised in %s' % (e.__class__.__name__, e, signature_repr(call))


@decorator
def log_durations(call, print_func):
    start = time.time()
    result = call()
    end = time.time()

    print_func("%s in %s" % (format_time(end - start), signature_repr(call)))
    return result

print_durations = log_durations(print)


def format_time(sec):
    if sec < 1e-6:
        return '%6.2f ns' % (sec * 1e9)
    elif sec < 1e-3:
        return '%6.2f µs' % (sec * 1e6)
    elif sec < 1:
        return '%6.2f ms' % (sec * 1e3)
    else:
        return '%6.2f s' % sec


### Call signature stringification utils

MAX_REPR_LEN = 25

def signature_repr(call):
    args_repr = imap(smart_repr, call._args)
    kwargs_repr = ('%s=%s' % (key, smart_repr(value)) for key, value in call._kwargs.items())
    return '%s(%s)' % (call._func.__name__, ', '.join(chain(args_repr, kwargs_repr)))

def smart_repr(value):
    if isinstance(value, basestring):
        res = repr(value)
    else:
        res = str(value)

    # res = res.replace('\n', ' ')
    res = re.sub(r'\s+', ' ', res)
    if len(res) > MAX_REPR_LEN:
        res = res[:MAX_REPR_LEN-3] + '...'
    return res
