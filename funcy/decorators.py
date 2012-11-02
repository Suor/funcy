import inspect
from functools import wraps


def _func_decorator(deco, dargs=(), dkwargs={}):
    assert not dkwargs # not sure how and whether this should work
    def _decorator(func):
        def wrapper(*args, **kwargs):
            return deco(func, *(dargs + args), **kwargs)
        return wraps(func)(wrapper)
    return _decorator

def _gen_decorator(gen, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            for _ in gen(*dargs, **dkwargs):
                func(*args, **kwargs)
        return wraps(func)(wrapper)
    return _decorator


def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))

def decorator(deco):
    if inspect.isgeneratorfunction(deco):
        fab = _gen_decorator
        args = argcounts(deco) != (0, False, False)
    else:
        fab = _func_decorator
        args = argcounts(deco) != (1, False, False)

    if args:
        def decorator_fab(*dargs, **dkwargs):
            return fab(deco, dargs, dkwargs)
        return wraps(deco)(decorator_fab)
    else:
        return wraps(deco)(fab(deco))
