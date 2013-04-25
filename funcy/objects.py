from functools import wraps

from .strings import cut_prefix


__all__ = ['cached_property', 'monkey']


def cached_property(func):
    @property
    @wraps(func)
    def wrapper(self):
        attname = '_' + func.__name__
        if not hasattr(self, attname):
            setattr(self, attname, func(self))
        return getattr(self, attname)
    return wrapper


def monkey(cls):
    assert isinstance(cls, type), "Attempting to monkey patch non-class"

    def decorator(value):
        func = getattr(value, 'fget', value) # Support properties
        name = cut_prefix(func.__name__, '%s__' % cls.__name__)

        func.__name__ = name
        func.original = getattr(cls, name, None)

        setattr(cls, name, value)
        return value
    return decorator
