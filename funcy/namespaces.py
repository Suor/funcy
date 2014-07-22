from .colls import walk_values
from .funcs import iffy


__all__ = ('namespace',)


class namespace_meta(type):
    def __new__(cls, name, bases, attrs):
        attrs = walk_values(iffy(callable, staticmethod), attrs)
        return super(namespace_meta, cls).__new__(cls, name, bases, attrs)

class namespace(object):
    __metaclass__ = namespace_meta
