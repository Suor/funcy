from __builtin__ import all as _all, any as _any
from collections import Mapping, Set, Iterable, Iterator
from itertools import ifilter, imap, chain

from .funcs import complement


__all__ = ['empty', 'iteritems', 'join', 'merge',
           'walk', 'walk_keys', 'walk_values', 'select', 'select_keys', 'select_values',
           'is_distinct', 'all', 'any', 'none', 'some',
           'zipdict', 'flip', 'project']


### Generic ops
def empty(coll):
    return coll.__class__()

# postponed - not sure if it's usefull
# def not_empty(coll):
#     return coll or None

# polluting? this is a common variable name
# posponed - since you should walk away with iteritems in most cases
# def items(coll):
#     return coll.items() if hasattr(coll, 'items') else coll

def iteritems(coll):
    return coll.iteritems() if hasattr(coll, 'iteritems') else coll


def join(colls):
    it = iter(colls)
    dest = next(colls, None)
    if dest is None:
        raise TypeError('join needs at least one collection or string')
    cls = dest.__class__

    if isinstance(dest, basestring):
        return ''.join(colls)
    elif isinstance(dest, Mapping):
        return reduce(lambda a, b: cls(a, **b), colls)
    elif isinstance(dest, Set):
        return dest.union(*it)
    elif isinstance(dest, (Iterator, xrange)):
        return chain.from_iterable(colls)
    elif isinstance(dest, Iterable):
        return cls(chain.from_iterable(colls)) # could be reduce(concat, ...)
                                               # more effective for low count
    else:
        raise TypeError("Don't know how to join %s" % cls.__name__)

def merge(*colls):
    return join(colls)

# postponed
# def conj(coll, *xs):
#     return merge(coll, xs)


def walk(f, coll):
    """
    Walk coll transforming it's elements with f.
    Same as map, but preserves coll type.
    """
    return coll.__class__(imap(f, iteritems(coll)))

def walk_keys(f, coll):
    return walk(lambda (k, v): (f(k), v), coll)

def walk_values(f, coll):
    return walk(lambda (k, v): (k, f(v)), coll)

# TODO: prewalk, postwalk and friends

def select(f, coll):
    """Same as filter but preserves coll type."""
    return coll.__class__(ifilter(f, iteritems(coll)))

def select_keys(f, coll):
    return select(lambda (k, v): f(k), coll)

def select_values(f, coll):
    return select(lambda (k, v): f(v), coll)

### Content tests

def is_distinct(coll):
    return len(coll) == len(set(coll))


def all(pred, coll=None):
    if coll is None:
        return _all(pred)
    return _all(imap(pred, coll))

def any(pred, coll=None):
    if coll is None:
        return _any(pred)
    return _any(imap(pred, coll))

none = complement(any)

# Not same as in clojure! returns value found not pred(value)
# NOTE: should I name it "find" when pred is here
def some(pred, coll=None):
    if coll is None:
        return some(None, pred)
    return next(ifilter(pred, coll), None)

# TODO: vector comparison tests - ascending, descending and such

# TODO: capabilities + type tests or skip?

def zipdict(keys, vals):
    return dict(zip(keys, vals))

def flip(mapping):
    return walk(lambda (k, v): (v, k), mapping)

def project(mapping, keys):
    return mapping.__class__((k, mapping[k]) for k in keys if k in mapping)


from whatever import _


def test_walk_values():
    assert walk_values(_ * 2, {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}

def test_select_values():
    assert select_values(_ % 2, {'a': 1, 'b': 2}) == {'a': 1}

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
