from operator import __not__
# NOTE: there are some alternate implementations commented out here
#       just keep them for alpha until I realize some things:
#           - when I should just stop decomposing?
#           - how much point-free notation should be used?
#           - how much optimization should I impose?
#           - should I use defs over lambdas and point-free notation for better introspection?



identity = lambda x: x
constantly = lambda x: lambda *a, **kw: x
# This one is implemented with * syntax in python
# Do we need this entity as explicit function?
# pack = lambda *fs: fs

# an operator.methodcaller() brother
caller = lambda *a, **kw: lambda f: f(*a, **kw)

# not using functools.partial to get real function
def partial(func, *args, **kwargs):
    def new_func(*fargs, **fkwargs):
        return func(*(args + fargs), **dict(kwargs, **fkwargs))
    new_func.func = func
    new_func.args = args
    new_func.kwargs = kwargs
    return new_func

_compose_pair = lambda f, g: lambda *a, **kw: f(g(*a, **kw))
compose = lambda *fs: reduce(_compose_pair, fs, identity)
# comp = partial(reduce, _compose_pair) # packed args variant, probably, bad idea
                                        # also does not support comp([])
# compose = _compose_pair(comp, pack)

complement = lambda f: compose(__not__, f)
# complement = partial(compose, __not__)

# NOTE: move these to .funcdata or .funcolls or .fdata?
def _map_over(coll):
    return lambda f: map(f, coll)

def juxt(*fs):
    # return lambda *a, **kw: map(caller(*a, **kw), fs)
    return compose(_map_over(fs), caller)



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
