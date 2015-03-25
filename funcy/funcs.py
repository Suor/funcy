from operator import __not__
from functools import reduce

from .cross import map, imap
from .simple_funcs import *
from .simple_funcs import __all__ as all_simple
from .funcmakers import make_func


__all__ = all_simple + ['compose', 'rcompose', 'complement', 'juxt', 'ijuxt']


def compose(*fs):
    if fs:
        pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
        return reduce(pair, imap(make_func, fs))
    else:
        return identity

def rcompose(*fs):
    return compose(*reversed(fs))

def complement(pred):
    return compose(__not__, pred)


# NOTE: using lazy map in these two will result in empty list/iterator
#       from all calls to i?juxt result since map iterator will be depleted

def juxt(*fs):
    extended_fs = map(make_func, fs)
    return lambda *a, **kw: [f(*a, **kw) for f in extended_fs]

def ijuxt(*fs):
    extended_fs = map(make_func, fs)
    return lambda *a, **kw: (f(*a, **kw) for f in extended_fs)
