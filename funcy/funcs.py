from operator import __not__

from .simple_funcs import *
from .funcmakers import make_func


__all__ = ['identity', 'constantly', 'caller',
           'partial', 'curry', 'compose', 'complement',
           'juxt', 'ijuxt',
           'iffy']


# NOTE: could be optimized in two ways:
#       1. Don't use an `identity` in reduce if fs is not empty.
#       2. Use special `pair` version depending on fs[-1] signature.
def compose(*fs):
    pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
    return reduce(pair, map(make_func, fs), identity)

def complement(pred):
    return compose(__not__, pred)

def juxt(*fs):
    extended_fs = map(make_func, fs)
    return lambda *a, **kw: [f(*a, **kw) for f in extended_fs]

def ijuxt(*fs):
    extended_fs = map(make_func, fs)
    return lambda *a, **kw: (f(*a, **kw) for f in extended_fs)

