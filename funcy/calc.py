from datetime import datetime, timedelta
import inspect

from .decorators import wraps
from .cross import PY2

__all__ = ['memoize', 'make_lookuper', 'silent_lookuper', 'cache']


# TODO: guard from keyword arguments in memoize, cache and make_lookuper.
#       For now it's complicated to do in python 2/3 compatible mode,
#       thanks getargspec/getfullargspec/signature mess.


class SkipMemoization(Exception):
    pass


def memoize(func):
    memory = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs:
            key = args + tuple(sorted(kwargs.items()))
        else:
            key = args
        try:
            return memory[key]
        except KeyError:
            try:
                value = memory[key] = func(*args, **kwargs)
                return value
            except SkipMemoization as e:
                return e.args[0] if e.args else None
    return wrapper
memoize.skip = SkipMemoization


def _make_lookuper(silent):
    def make_lookuper(func):
        has_args, has_keys = has_arg_types(func)
        assert not has_keys, \
            'Lookup table building function should not have keyword arguments'

        if has_args:
            @memoize
            def wrapper(*args):
                f = lambda: func(*args)
                f.__name__ = '%s(%s)' % (func.__name__, ', '.join(map(str, args)))
                return make_lookuper(f)
        else:
            memory = {}

            def wrapper(arg):
                if not memory:
                    memory[object()] = None # prevent continuos memory refilling
                    memory.update(func())

                if silent:
                    return memory.get(arg)
                elif arg in memory:
                    return memory[arg]
                else:
                    raise LookupError("Failed to look up %s(%s)" % (func.__name__, arg))

        return wraps(func)(wrapper)
    return make_lookuper

make_lookuper = _make_lookuper(False)
silent_lookuper = _make_lookuper(True)


def cache(timeout):
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args):
            if args in cache:
                result, timestamp = cache[args]
                if datetime.now() - timestamp < timeout:
                    return result
                else:
                    del cache[args]

            result = func(*args)
            cache[args] = result, datetime.now()
            return result

        def invalidate(*args):
            cache.pop(args)
        wrapper.invalidate = invalidate

        def invalidate_all():
            cache.clear()
        wrapper.invalidate_all = invalidate_all

        return wrapper
    return decorator


if PY2:
    def has_arg_types(func):
        spec = inspect.getargspec(func)
        return bool(spec.args or spec.varargs), bool(spec.keywords)
else:
    def has_arg_types(func):
        params = inspect.signature(func).parameters.values()
        return any(p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD, p.VAR_POSITIONAL)
                   for p in params), \
               any(p.kind in (p.KEYWORD_ONLY, p.VAR_KEYWORD) for p in params)
