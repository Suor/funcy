import inspect
from functools import wraps


__all__ = ['decorator']


def make_call(func, args, kwargs):
    call = lambda: func(*args, **kwargs)
    # Support args and func introspection
    call.func = func
    call.args = args
    call.kwargs = kwargs
    return call

def make_call_decorator(deco, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            call = make_call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)
    return _decorator

def make_gen_decorator(gen, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            # TODO: collect function results?
            for _ in gen(*dargs, **dkwargs):
                func(*args, **kwargs)
        return wraps(func)(wrapper)
    return _decorator


def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))

def decorator(deco):
    # TODO: make uncalled deco usable as deco called with all defaults
    #       when it has defaults for all arguments
    if inspect.isgeneratorfunction(deco):
        fab = make_gen_decorator
        args = argcounts(deco) != (0, False, False)
    else:
        fab = make_call_decorator
        args = argcounts(deco) != (1, False, False)

    if args:
        def decorator_fab(*dargs, **dkwargs):
            return fab(deco, dargs, dkwargs)
        return wraps(deco)(decorator_fab)
    else:
        return wraps(deco)(fab(deco))
