from operator import itemgetter

from .compat import basestring, Mapping, Set
from .strings import re_tester, re_finder, _re_type


__all__ = ('make_func', 'make_pred')


def make_func(f, builtin=False, test=False):
    if callable(f):
        return f
    elif f is None:
        # pass None to builtin as predicate or mapping function for speed
        return None if builtin else \
               bool if test else lambda x: x
    elif isinstance(f, (basestring, _re_type)):
        return re_tester(f) if test else re_finder(f)
    elif isinstance(f, (int, slice)):
        return itemgetter(f)
    elif isinstance(f, Mapping):
        return f.__getitem__
    elif isinstance(f, Set):
        return f.__contains__
    else:
        raise TypeError("Can't make a func from %s" % f.__class__.__name__)

def make_pred(pred, builtin=False):
    return make_func(pred, builtin=builtin, test=True)
