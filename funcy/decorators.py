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
    # NOTE: we use class enclosed this way instead of creating normal object with attributes
    #       cause it's much faster
    class Call(object):
        def __call__(self, *a, **kw):
            return func(*(args + a), **dict(kwargs, **kw))

        _args = args
        _kwargs = kwargs
        _func = func

        def __getattr__(self, name):
            if not inspect.isfunction(func):
                raise TypeError("Can't introspect argument %s for non-function" % name)
            if not self.__dict__:
                self.__dict__ = inspect.getcallargs(func, *args, **kwargs)
            try:
                return self.__dict__[name]
            except KeyError:
                raise NameError("Function %s does not have argument %s" \
                                % (func.__name__, name))

    return Call()


def argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))

