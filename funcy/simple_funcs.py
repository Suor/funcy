from functools import partial

from .primitives import EMPTY
from ._inspect import get_required_args


__all__ = ['identity', 'constantly', 'caller',
           'partial', 'rpartial', 'func_partial',
           'curry', 'rcurry', 'autocurry',
           'iffy']


def identity(x):
    return x

def constantly(x):
    return lambda *a, **kw: x

# an operator.methodcaller() brother
def caller(*a, **kw):
    return lambda f: f(*a, **kw)

# not using functools.partial to get real function
def func_partial(func, *args, **kwargs):
    """
    A functools.partial alternative, which returns a real function.
    Can be used to construct methods.
    """
    return lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))

def rpartial(func, *args):
    return lambda *a: func(*(a + args))


def curry(func, n=EMPTY):
    if n is EMPTY:
        n = len(get_required_args(func))

    if n <= 1:
        return func
    elif n == 2:
        return lambda x: lambda y: func(x, y)
    else:
        return lambda x: curry(partial(func, x), n - 1)


def rcurry(func, n=EMPTY):
    if n is EMPTY:
        n = len(get_required_args(func))

    if n <= 1:
        return func
    elif n == 2:
        return lambda x: lambda y: func(y, x)
    else:
        return lambda x: rcurry(rpartial(func, x), n - 1)


def autocurry(func, n=EMPTY, required_args=EMPTY, _args=(), _kwargs={}):
    if required_args is EMPTY:
        required_args = get_required_args(func) if n is EMPTY else '*' * n

    def autocurried(*a, **kw):
        args = _args + a
        kwargs = _kwargs.copy()
        kwargs.update(kw)

        if len(args) + len(set(kwargs) & set(required_args)) >= len(required_args):
            return func(*args, **kwargs)
        else:
            return autocurry(func, required_args=required_args, _args=args, _kwargs=kwargs)

    return autocurried


def iffy(pred, action=EMPTY, default=identity):
    if action is EMPTY:
        return iffy(bool, pred)
    else:
        return lambda v: action(v)  if pred(v) else           \
                         default(v) if callable(default) else \
                         default
