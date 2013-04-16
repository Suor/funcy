from operator import __not__
from itertools import ifilter


__all__ = ['identity', 'constantly', 'caller',
           'partial', 'curry', 'compose', 'complement',
           'juxt', 'ijuxt',
           'iffy']


EMPTY = object()


def identity(x):
    return x

def constantly(x):
    return lambda *a, **kw: x

# an operator.methodcaller() brother
def caller(*a, **kw):
    return lambda f: f(*a, **kw)

# not using functools.partial to get real function
def partial(func, *args, **kwargs):
    return lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))

def curry(func, n=EMPTY):
    if n is EMPTY:
        n = func.__code__.co_argcount

    if n <= 1:
        return func
    elif n == 2:
        return lambda x: lambda y: func(x, y)
    else:
        return lambda x: curry(lambda *y: func(x, *y), n - 1)

# NOTE: could be optimized in two ways:
#       1. Don't use an `identity` in reduce if fs is not empty.
#       2. Use special `pair` version depending on fs[-1] signature.
def compose(*fs):
    pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
    return reduce(pair, fs, identity)

def complement(pred):
    return compose(__not__, pred)

def juxt(*fs):
    return lambda *a, **kw: [f(*a, **kw) for f in fs]

def ijuxt(*fs):
    return lambda *a, **kw: (f(*a, **kw) for f in fs)

def iffy(pred, action=EMPTY, default=identity):
    if action is EMPTY:
        return iffy(bool, pred)
    else:
        return lambda v: action(v)  if pred(v) else           \
                         default(v) if callable(default) else \
                         default
