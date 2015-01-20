from inspect import isclass, ismodule

from .strings import cut_prefix


__all__ = ['cached_property', 'monkey']


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into
    a property cached on the instance.
    """
    # NOTE: implementation borrowed from Django.
    # NOTE: we use fget, fset and fdel attributes to mimic @property.
    fset = fdel = None

    def __init__(self, fget):
        self.fget = fget
        self.__doc__ = getattr(fget, '__doc__')

    def __get__(self, instance, type=None):
        if instance is None:
            return self
        res = instance.__dict__[self.fget.__name__] = self.fget(instance)
        return res


def monkey(cls, name=None):
    assert isclass(cls) or ismodule(cls), "Attempting to monkey patch non-class and non-module"

    def decorator(value):
        func = getattr(value, 'fget', value) # Support properties
        func_name = name or cut_prefix(func.__name__, '%s__' % cls.__name__)

        func.__name__ = func_name
        func.original = getattr(cls, func_name, None)

        setattr(cls, func_name, value)
        return value
    return decorator


# TODO: monkey_mix()?
