from datetime import datetime, timedelta
import inspect

from .decorators import wraps
from .compat import PY2

__all__ = ['memoize', 'make_lookuper', 'silent_lookuper', 'cache']



class SkipMemoization(Exception):
    pass

# TODO: use real kwonly once in Python 3 only
def memoize(*args, **kwargs):
    """@memoize(key_func=None). Makes decorated function memoize its results.

    If key_func is specified uses key_func(*func_args, **func_kwargs) as memory key.
    Otherwise uses args + tuple(sorted(kwargs.items()))

    Exposes its memory via .memory attribute.
    """
    if args:
        assert len(args) == 1
        assert not kwargs
        return memoize()(args[0])
    key_func = kwargs.pop('key_func', None)
    if kwargs:
        raise TypeError('memoize() got unexpected keyword arguments: %s', ', '.join(kwargs))

    def decorator(func):
        memory = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            # NOTE: we inline this here but not in @cache,
            #       since @memoize also targets microoptimizations.
            key = key_func(*args, **kwargs) if key_func else \
                  args + tuple(sorted(kwargs.items())) if kwargs else args
            try:
                return memory[key]
            except KeyError:
                try:
                    value = memory[key] = func(*args, **kwargs)
                    return value
                except SkipMemoization as e:
                    return e.args[0] if e.args else None

        wrapper.memory = memory
        return wrapper
    return decorator

memoize.skip = SkipMemoization


def _make_lookuper(silent):
    def make_lookuper(func):
        """
        Creates a single argument function looking up result in a memory.

        Decorated function is called once on first lookup and should return all available
        arg-value pairs.

        Resulting function will raise LookupError when using @make_lookuper
        or simply return None when using @silent_lookuper.
        """
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
silent_lookuper.__name__ = 'silent_lookuper'


def cache(timeout, key_func=None):
    """Caches a function results for timeout seconds."""
    if isinstance(timeout, int):
        timeout = timedelta(seconds=timeout)

    if key_func is None:
        key_func = lambda *a, **kw: a + tuple(sorted(kw.items())) if kw else a

    def decorator(func):
        cache = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            if key in cache:
                result, timestamp = cache[key]
                if datetime.now() - timestamp < timeout:
                    return result
                else:
                    del cache[key]

            result = func(*args, **kwargs)
            cache[key] = result, datetime.now()
            return result

        def invalidate(*args, **kwargs):
            cache.pop(key_func(*args, **kwargs))
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
