import sys, inspect
from functools import partial

from .calc import memoize


__all__ = ['decorator']


def decorator(deco):
    # Any arguments after first become decorator arguments
    has_args = get_argcounts(deco) != (1, False, False)

    if has_args:
        # A decorator with arguments is essentialy a decorator fab
        def decorator_fab(*dargs, **dkwargs):
            return make_decorator(deco, dargs, dkwargs)
        return wraps(deco)(decorator_fab)
    else:
        return wraps(deco)(make_decorator(deco))


def make_decorator(deco, dargs=(), dkwargs={}):
    def _decorator(func):
        def wrapper(*args, **kwargs):
            call = Call(func, args, kwargs)
            return deco(call, *dargs, **dkwargs)
        return wraps(func)(wrapper)
    return _decorator


class Call(object):
    """
    A call object to pass as first argument to decorator.
    Call object is just a proxy for decorated function with call arguments saved in its attributes.
    """
    def __init__(self, func, args, kwargs):
        self._func, self._args, self._kwargs = func, args, kwargs
        self._introspected = False

    def __call__(self, *a, **kw):
        if not a and not kw:
            return self._func(*self._args, **self._kwargs)
        else:
            return self._func(*(self._args + a), **dict(self._kwargs, **kw))

    def __getattr__(self, name):
        try:
            res = self.__dict__[name] = arggetter(self._func)(name, self._args, self._kwargs)
            return res
        except TypeError as e:
            raise AttributeError(*e.args)


def get_argcounts(func):
    spec = inspect.getargspec(func)
    return (len(spec.args), bool(spec.varargs), bool(spec.keywords))

def get_argnames(func):
    func = unwrap(func)
    return func.__code__.co_varnames[:func.__code__.co_argcount]

@memoize
def arggetter(func):
    argnames = get_argnames(func)
    argcount = len(argnames)

    def get_arg(name, args, kwargs):
        if name not in argnames:
            raise TypeError("%s() doesn't have argument named %s" % (func.__name__, name))
        else:
            if name in kwargs:
                return kwargs[name]
            elif name in argnames:
                index = argnames.index(name)
                if index < len(args):
                    return args[index]
                else:
                    return func.__defaults__[index - argcount]

    return get_arg


### Fix functools.wraps to make it safely work with callables without all the attributes

# These are already safe in python 3.4 and __wrapped__ works the new way
if sys.version_info >= (3, 4):
    from functools import update_wrapper, wraps
else:
    # These are for python 2, so list of attributes is far shorter.
    # Python 3.2 and ealier will get reduced functionality, but we don't support it :)
    WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__doc__')
    WRAPPER_UPDATES = ('__dict__',)
    # Copy-pasted these two from python 3.3 functools source code
    def update_wrapper(wrapper,
                       wrapped,
                       assigned = WRAPPER_ASSIGNMENTS,
                       updated = WRAPPER_UPDATES):
        wrapper.__wrapped__ = wrapped
        for attr in assigned:
            try:
                value = getattr(wrapped, attr)
            except AttributeError:
                pass
            else:
                setattr(wrapper, attr, value)
        for attr in updated:
            getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
        # Return the wrapper so this can be used as a decorator via partial()
        return wrapper

    def wraps(wrapped,
              assigned = WRAPPER_ASSIGNMENTS,
              updated = WRAPPER_UPDATES):
        return partial(update_wrapper, wrapped=wrapped,
                       assigned=assigned, updated=updated)


### Backport of python 3.4 inspect.unwrap utility

try:
    from inspect import unwrap
except ImportError:
    # A simplified version, no stop keyword-only argument
    def unwrap(func):
        f = func  # remember the original func for error reporting
        memo = set([id(f)]) # Memoise by id to tolerate non-hashable objects
        while hasattr(func, '__wrapped__'):
            func = func.__wrapped__
            id_func = id(func)
            if id_func in memo:
                raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
            memo.add(id_func)
        return func

