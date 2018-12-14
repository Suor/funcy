from inspect import isclass, ismodule

from .compat import PY2
from .colls import walk_values
from .funcs import iffy
from .strings import cut_prefix


__all__ = ['cached_property', 'monkey', 'namespace', 'LazyObject', 'SingletonMeta']


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
    """
    Monkey patches class or module by adding to it decorated function.

    Anything overwritten could be accessed via .original attribute of decorated object.
    """
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


class namespace_meta(type):
    def __new__(cls, name, bases, attrs):
        attrs = walk_values(iffy(callable, staticmethod), attrs)
        return super(namespace_meta, cls).__new__(cls, name, bases, attrs)

class namespace(object):
    """A base class that prevents its member functions turning into methods."""
    if PY2:
        __metaclass__ = namespace_meta


class LazyObject(object):
    """
    A simplistic lazy init object.
    Rewrites itself when any attribute is accesssed.
    """
    # NOTE: we can add lots of magic methods here to intercept on more events,
    #       this is postponed. As well as metaclass to support isinstance() check.
    def __init__(self, init):
        self.__dict__['_init'] = init

    def _setup(self):
        obj = self._init()
        object.__setattr__(self, '__class__', obj.__class__)
        object.__setattr__(self, '__dict__', obj.__dict__)

    def __getattr__(self, name):
        self._setup()
        return getattr(self, name)

    def __setattr__(self, name, value):
        self._setup()
        return setattr(self, name, value)


class SingletonMeta(type):
    """Metaclass for creating Singleton"""

    @staticmethod
    def __new__(mcs, cls_name, bases, attrs):
        cls = super(SingletonMeta, mcs).__new__(mcs, cls_name, bases, attrs)
        original_new = cls.__new__

        def new(cls, *args, **kwargs):
            if cls.__instance is None:
                instance = original_new(cls, *args, **kwargs)
                cls.__instance = instance
            return cls.__instance

        cls.__instance = None
        cls.__new__ = staticmethod(new)

        return cls
