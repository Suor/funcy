from inspect import isclass, ismodule

from .strings import cut_prefix


__all__ = ['cached_property', 'monkey']


def cached_property(func):
    cache_attname = '_' + func.__name__

    def getter(self):
        if not hasattr(self, cache_attname):
            setattr(self, cache_attname, func(self))
        return getattr(self, cache_attname)

    def setter(self, value):
        setattr(self, cache_attname, value)

    return property(getter, setter)


def monkey(cls):
    assert isclass(cls) or ismodule(cls), "Attempting to monkey patch non-class and non-module"

    def decorator(value):
        func = getattr(value, 'fget', value) # Support properties
        name = cut_prefix(func.__name__, '%s__' % cls.__name__)

        func.__name__ = name
        func.original = getattr(cls, name, None)

        setattr(cls, name, value)
        return value
    return decorator


# TODO: monkey_mix()?
