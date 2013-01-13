from __builtin__ import all as _all, any as _any
from operator import itemgetter, methodcaller
from collections import Mapping, Set, Iterable, Iterator, defaultdict
from itertools import ifilter, imap, chain, tee

from .funcs import partial, complement
from .seqs import take


__all__ = ['empty', 'iteritems', 'join', 'merge',
           'walk', 'walk_keys', 'walk_values', 'select', 'select_keys', 'select_values',
           'is_distinct', 'all', 'any', 'none', 'one', 'some',
           'zipdict', 'flip', 'project',
           'where', 'pluck', 'invoke']


### Generic ops
def _factory(coll):
    # Hack for defaultdicts overriden constructor
    if isinstance(coll, defaultdict):
        return partial(defaultdict, coll.default_factory)
    elif isinstance(coll, basestring):
        return ''.join
    else:
        return coll.__class__

def empty(coll):
    return _factory(coll)()

# TODO: not_empty/non_empty working with iterators?
#       kinda bool(iterator)
# NOTE: should I add it to seqs or even data?

def iteritems(coll):
    return coll.iteritems() if hasattr(coll, 'iteritems') else coll


def join(colls):
    colls, colls_copy = tee(colls)
    it = iter(colls_copy)
    dest = next(it, None)
    if dest is None:
        return None
    cls = dest.__class__

    if isinstance(dest, basestring):
        return ''.join(colls)
    elif isinstance(dest, Mapping):
        return reduce(lambda a, b: _factory(dest)(a, **b), colls)
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
    return _factory(coll)(imap(f, iteritems(coll)))

def walk_keys(f, coll):
    return walk(lambda (k, v): (f(k), v), coll)

def walk_values(f, coll):
    return walk(lambda (k, v): (k, f(v)), coll)

# TODO: prewalk, postwalk and friends

def select(pred, coll):
    """Same as filter but preserves coll type."""
    return _factory(coll)(ifilter(pred, iteritems(coll)))

def select_keys(pred, coll):
    return select(lambda (k, v): pred(k), coll)

def select_values(pred, coll):
    return select(lambda (k, v): pred(v), coll)

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

def one(pred, coll=None):
    if coll is None:
        return one(bool, pred)
    return len(take(2, ifilter(pred, coll))) == 1

# Not same as in clojure! returns value found not pred(value)
# NOTE: should I name it "find" when pred is here
def some(pred, coll=None):
    if coll is None:
        return some(None, pred)
    return next(ifilter(pred, coll), None)

# TODO: a variant of some that returns mapped value,
#       one can use some(imap(f, seq)) or first(ikeep(f, seq)) for now.
#       Call it `find`?

# TODO: vector comparison tests - ascending, descending and such

# TODO: capabilities + type tests or skip?

def zipdict(keys, vals):
    return dict(zip(keys, vals))

def flip(mapping):
    return walk(lambda (k, v): (v, k), mapping)

def project(mapping, keys):
    return _factory(mapping)((k, mapping[k]) for k in keys if k in mapping)


def where(mappings, **cond):
    match = lambda m: all(m[k] == v for k, v in cond.items())
    return filter(match, mappings)

# NOTE: should I change params order to be more consistent with map/filter
#       or leave as is to be consistent with where/invoke?
def pluck(mappings, key):
    return map(itemgetter(key), mappings)


def invoke(objects, name, *args, **kwargs):
    return map(methodcaller(name, *args, **kwargs), objects)
