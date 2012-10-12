import inspect
from functools import wraps

# TODO: refactor, rethink or get rid of
# NOTE: will, probably need some kind of eval or byteplay to make this really work
#       the other way is simulate argspec,
#       now we are ignoring it, which is error prone and don't works with default values

def _make_decorator(deco, deco_args=()):
    @wraps(deco)
    def forged_deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return deco(func, *(deco_args + args), **kwargs)
        return wrapper
    return forged_deco

def decorator(deco):
    deco_arg_names = inspect.getargspec(deco).args[1:]
    if deco_arg_names:
        @wraps(deco)
        def forged_deco_fab(*deco_args):
            # check args and fill defaults
            return _make_decorator(deco, deco_args)
        return forged_deco_fab
    else:
        return _make_decorator(deco)

def _make_call_decorator(deco, deco_args=()):
    @wraps(deco)
    def forged_deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            call = lambda: func(*args, **kwargs)
            return deco(call, *deco_args)
        return wrapper
    return forged_deco

def call_decorator(deco):
    deco_arg_names = inspect.getargspec(deco).args[1:]
    if deco_arg_names:
        @wraps(deco)
        def forged_deco_fab(*deco_args):
            return _make_call_decorator(deco, deco_args)
        return forged_deco_fab
    else:
        return _make_call_decorator(deco)

