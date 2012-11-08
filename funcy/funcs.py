from operator import __not__
from itertools import ifilter


__all__ = ['identity', 'constantly', 'caller',
           'partial', 'compose', 'complement',
           'juxt', 'ijuxt']


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

def compose(*fs):
    pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
    return reduce(pair, fs, identity)

def complement(f):
    return compose(__not__, f)

def juxt(*fs):
    return lambda *a, **kw: [f(*a, **kw) for f in fs]

def ijuxt(*fs):
    return lambda *a, **kw: (f(*a, **kw) for f in fs)


from operator import __add__, __sub__
from whatever import _


def test_caller():
    assert caller([1, 2])(sum) == 3

def test_compose():
    double = _ * 2
    inc    = _ + 1
    assert compose(inc, double)(10) == 21
    assert compose(str, inc, double)(10) == '21'

def test_complement():
    assert complement(identity)(0) == True
    assert complement(identity)([1, 2]) == False

def test_partial():
    assert partial(__add__, 10)(1) == 11
    assert partial(__add__, 'abra')('cadabra') == 'abracadabra'

    merge = lambda a=None, b=None: a + b
    assert partial(merge, a='abra')(b='cadabra') == 'abracadabra'
    assert partial(merge, b='abra')(a='cadabra') == 'cadabraabra'

def test_juxt():
    assert juxt(__add__, __sub__)(10, 2) == [12, 8]
