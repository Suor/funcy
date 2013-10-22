import inspect
from functools import wraps


__all__ = ['decorator']


def decorator(deco):
    # Any arguments after first become decorator arguments
    args = argcounts(deco) != (1, False, False)

    if args:
        # A decorator with arguments is essentialy a decorator fab
        def decorator_fab(*dargs, **dkwargs):
            return make_decorator(deco, dargs, dkwargs)
        return wraps(deco)(decorator_fab)
    else:
        return wraps(deco)(make_decorator(deco))


def make_decorator(deco, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            call = make_call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)
    return _decorator


def make_call(func, args, kwargs):
    """
    Constructs a call object to pass as first argument to decorator.
    Call object is just a proxy for decorated function with call arguments saved in its attributes.
    """
    call = lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))

    # Support args and func introspection
    call._func = func
    call._args = args
    call._kwargs = kwargs

    # Save actual arg values on call "object" with their names as attributes for easier access
    if inspect.isfunction(func):
        call_args = inspect.getcallargs(func, *args, **kwargs)
        for arg_name, arg_value in call_args.items():
            setattr(call, arg_name, arg_value)

    return call


def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))

