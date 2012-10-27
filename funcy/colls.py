from __builtin__ import all as _all, any as _any
from itertools import ifilter, imap, chain

from .funcs import complement


### Generic ops
# count = len

def empty(coll):
    return coll.__class__()

def not_empty(coll):
    return coll or None

def into(dest, src):
    if hasattr(dest, 'update'):
        result = dest.copy()
        result.update(src)
        return result
    elif hasattr(dest, 'union'):
        return dest.union(src)
    elif hasattr(dest, '__add__'):
        return dest + dest.__class__(src)
    elif hasattr(dest, '__iter__'):
        return chain(dest, src)
    else:
        raise TypeError("Don't know how to add items to %s" % dest.__class__.__name__)

def conj(coll, *xs):
    return into(coll, xs)

def walk(f, coll):
    """
    Walk coll transforming it's elements with f.
    Same as map, but preserves coll type.
    """
    items = coll.iteritems() if hasattr(coll, 'iteritems') else coll
    return coll.__class__(imap(f, items))

def walk_keys(f, coll):
    return walk(lambda (k, v): (f(k), v), coll)

def walk_values(f, coll):
    return walk(lambda (k, v): (k, f(v)), coll)

# TODO: prewalk, postwalk and friends


### Content tests

def is_distinct(coll):
    return len(coll) == len(set(coll))

# NOTE: maybe not a greatest implementation but works for iterators.
#       Though, it consumes an item from them which probably makes it useless.
#
#       Get rid of it and use boolean test instead?
def is_empty(coll):
    try:
        next(iter(coll))
        return False
    except StopIteration:
        return True

def all(pred, coll=None):
    if coll is None:
        return _all(pred)
    return _all(imap(pred, coll))

def any(pred, coll=None):
    if coll is None:
        return _any(pred)
    return _any(imap(pred, coll))

none = complement(any)

def some(pred, coll=None):
    if coll is None:
        return some(None, pred)
    return next(ifilter(pred, coll), None)


# TODO: capabilities + type tests or skip?


from whatever import _

def test_all():
    assert all([1,2,3])
    assert not all([1,2,''])
    assert all(callable, [abs, open, int])
    assert not all(_ < 3, [1,2,5])

def test_any():
    assert any([0, False, 3, ''])
    assert any([0, False, '']) == False
    assert any(_ > 0, [1,2,0])
    assert any(_ < 0, [1,2,0]) == False

def test_none():
    assert none([0, False])
    assert none(_ < 0, [0, -1]) == False

def test_some():
    assert some([0, '', 2, 3]) == 2
    assert some(_ > 3, range(10)) == 4
