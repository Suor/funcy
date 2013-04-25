import inspect
from functools import wraps


__all__ = ['decorator']


def make_call(func, args, kwargs):
    call = lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))

    # Support args and func introspection
    call._func = func
    call._args = args
    call._kwargs = kwargs

    # Save actual arg values on call "object"
    for arg_name, arg_value in inspect.getcallargs(func, *args, **kwargs).items():
        setattr(call, arg_name, arg_value)

    return call

def make_decorator(deco, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            call = make_call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)
    return _decorator

def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))

def decorator(deco):
    # Any arguments after first become decorator arguments
    args = argcounts(deco) != (1, False, False)

    if args:
        def decorator_fab(*dargs, **dkwargs):
            return make_decorator(deco, dargs, dkwargs)
        return wraps(deco)(decorator_fab)
    else:
        return wraps(deco)(make_decorator(deco))
