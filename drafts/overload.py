from functools import wraps
from itertools import starmap

__ALL__ = ['overload']

def check_arg(arg, spec):
    if isinstance(spec, (type, tuple)):
        return isinstance(arg, spec)
    elif callable(spec):
        return spec(arg)
    else:
        raise TypeError('Unknown argument spec %s' % repr(spec))

def check_spec(types, args):
    return len(types) == len(args) and all(starmap(check_arg, zip(args, types)))

def select_overloaded(func, args):
    for ts, f in func.overload:
        if check_spec(ts, args):
            return f
    else:
        argtypes = ', '.join(type(a).__name__ for a in args)
        raise TypeError('No overloaded version of %s() matching %s argument type(s)'
                            % (func.__name__, argtypes))

def overload(*types):
    def decorator(func):
        func.overload = getattr(func.__globals__.get(func.__name__), 'overload', [])
        func.overload.append((types, func))

        def wrapper(*args):
            return select_overloaded(func, args)(*args)
        return wraps(func)(wrapper)
    return decorator


import pytest
from whatever import _

@overload(int)
def quantify(n):
    return 'quantify' * n

@overload(str)
def quantify(s):
    return s * 2

@overload(str, int)
def quantify(s, n):
    return s * n

def test_quantify():
    assert quantify(2) == 'quantifyquantify'
    assert quantify('bye') == 'byebye'
    assert quantify('xy', 3) == 'xyxyxy'

    with pytest.raises(TypeError): quantify(1, 2, 3)
    with pytest.raises(TypeError): quantify([])
    with pytest.raises(TypeError): quantify('hi', 'bye')


@overload(int, int)
def step(start, step):
    return start + step

@overload(int, callable)
def step(start, succ):
    return succ(start)

def test_step():
    assert step(10, 3) == 13
    assert step(10, _*2) == 20
