from operator import __not__
from itertools import ifilter


def identity(x):
    return x

def constantly(x):
    return lambda *a, **kw: x

# an operator.methodcaller() brother
def caller(*a, **kw):
    return lambda f: f(*a, **kw)

# not using functools.partial to get real function
def partial(func, *args, **kwargs):
    def new_func(*fargs, **fkwargs):
        return func(*(args + fargs), **dict(kwargs, **fkwargs))
    new_func.func = func
    new_func.args = args
    new_func.kwargs = kwargs
    return new_func

def compose(*fs):
    pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
    return reduce(pair, fs, identity)

def complement(f):
    return compose(__not__, f)

def juxt(*fs):
    return lambda *a, **kw: [f(*a, **kw) for f in fs]

def ijuxt(*fs):
    return lambda *a, **kw: (f(*a, **kw) for f in fs)

# fnil ?

# NOTE: Should these ones be moved somewhere? func_colls? fcolls?
#       Should I call them every_pred, all_pred, any_pred ... ?
# every-pred in clojure
def all_fn(*fs):
    return compose(all, ijuxt(*fs))

def first(pred, coll=None):
    if coll is None:
        return first(None, pred)
    return next(ifilter(pred, coll), None)

# some-fn in clojure
def first_fn(*fs):
    return compose(first, ijuxt(*fs))

def any_fn(*fs):
    return compose(any, ijuxt(*fs))


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

def test_all_fn():
    assert filter(all_fn(_ > 3, _ % 2), range(10)) == [5, 7, 9]

def test_first_fn():
    assert first_fn(_-1, _*0, _+1, _*2)(1) == 2
