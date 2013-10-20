from .primitives import EMPTY


def identity(x):
    return x

def constantly(x):
    return lambda *a, **kw: x

# an operator.methodcaller() brother
def caller(*a, **kw):
    return lambda f: f(*a, **kw)

# not using functools.partial to get real function
def partial(func, *args, **kwargs):
    return lambda *a, **kw: func(*(args + a), **dict(kwargs, **kw))

def curry(func, n=EMPTY):
    if n is EMPTY:
        n = func.__code__.co_argcount

    if n <= 1:
        return func
    elif n == 2:
        return lambda x: lambda y: func(x, y)
    else:
        return lambda x: curry(lambda *y: func(x, *y), n - 1)

def iffy(pred, action=EMPTY, default=identity):
    if action is EMPTY:
        return iffy(bool, pred)
    else:
        return lambda v: action(v)  if pred(v) else           \
                         default(v) if callable(default) else \
                         default
