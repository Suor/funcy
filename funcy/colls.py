import sys
try:
    from __builtin__ import all as _all, any as _any
except ImportError:
    from builtins import all as _all, any as _any
from operator import itemgetter, methodcaller
from collections import Mapping, Set, Iterable, Iterator, defaultdict
from itertools import chain, tee
from functools import reduce

from .cross import basestring, xrange, izip
from .primitives import EMPTY
from .funcs import identity, partial, compose, complement
from .funcmakers import wrap_mapper, wrap_selector
from .seqs import take, ximap, ifilter


__all__ = ['empty', 'iteritems',
           'join', 'merge',
           'walk', 'walk_keys', 'walk_values', 'select', 'select_keys', 'select_values', 'compact',
           'is_distinct', 'all', 'any', 'none', 'one', 'some',
           'zipdict', 'flip', 'project', 'izip_values', 'izip_dicts',
           'where', 'pluck', 'invoke']


### Generic ops
def _factory(coll, mapper=None):
    # Hack for defaultdicts overriden constructor
    if isinstance(coll, defaultdict):
        item_factory = compose(mapper, coll.default_factory) if mapper else coll.default_factory
        return partial(defaultdict, item_factory)
    elif isinstance(coll, Iterator):
        return identity
    elif isinstance(coll, basestring):
        return ''.join
    else:
        return coll.__class__

def empty(coll):
    return _factory(coll)()

if sys.version_info[0] == 2:
    def iteritems(coll):
        return coll.iteritems() if hasattr(coll, 'iteritems') else coll
else:
    def iteritems(coll):
        return coll.items() if hasattr(coll, 'items') else coll


def join(colls):
    colls, colls_copy = tee(colls)
    it = iter(colls_copy)
    try:
        dest = next(it)
    except StopIteration:
        return None
    cls = dest.__class__

    if isinstance(dest, basestring):
        return ''.join(colls)
    elif isinstance(dest, Mapping):
        result = dest.copy()
        for d in it:
            result.update(d)
        return result
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


def join_with(f, dicts):
    dicts = list(dicts)
    if not dicts:
        return {}
    elif len(dicts) == 1:
        return dicts[0]

    lists = {}
    for c in dicts:
        for k, v in iteritems(c):
            if k in lists:
                lists[k].append(v)
            else:
                lists[k] = [v]

    if f is not list:
        # kind of walk_values() inplace
        for k, v in lists:
            lists[k] = f(v)

    return f

def merge_with(f, *dicts):
    return join_with(f, dicts)


def walk(f, coll):
    """
    Walk coll transforming it's elements with f.
    Same as map, but preserves coll type.
    """
    return _factory(coll)(ximap(f, iteritems(coll)))

@wrap_mapper
def walk_keys(f, coll):
    # NOTE: we use this awkward construct instead of lambda to be Python 3 compatible
    def pair_f(pair):
        k, v = pair
        return f(k), v

    return walk(pair_f, coll)

@wrap_mapper
def walk_values(f, coll):
    # NOTE: we use this awkward construct instead of lambda to be Python 3 compatible
    def pair_f(pair):
        k, v = pair
        return k, f(v)

    return _factory(coll, mapper=f)(ximap(pair_f, iteritems(coll)))

# TODO: prewalk, postwalk and friends

def select(pred, coll):
    """Same as filter but preserves coll type."""
    return _factory(coll)(ifilter(pred, iteritems(coll)))

@wrap_selector
def select_keys(pred, coll):
    return select(lambda pair: pred(pair[0]), coll)

@wrap_selector
def select_values(pred, coll):
    return select(lambda pair: pred(pair[1]), coll)


def compact(coll):
    if isinstance(coll, Mapping):
        return select_values(bool, coll)
    else:
        return select(bool, coll)


### Content tests

def is_distinct(coll, key=EMPTY):
    if key is EMPTY:
        return len(coll) == len(set(coll))
    else:
        return len(coll) == len(set(ximap(key, coll)))


def all(pred, seq=EMPTY):
    if seq is EMPTY:
        return _all(pred)
    return _all(ximap(pred, seq))

def any(pred, seq=EMPTY):
    if seq is EMPTY:
        return _any(pred)
    return _any(ximap(pred, seq))

none = complement(any)

def one(pred, seq=EMPTY):
    if seq is EMPTY:
        return one(bool, pred)
    return len(take(2, ifilter(pred, seq))) == 1

# Not same as in clojure! returns value found not pred(value)
def some(pred, seq=EMPTY):
    if seq is EMPTY:
        return some(bool, pred)
    return next(ifilter(pred, seq), None)

# TODO: a variant of some that returns mapped value,
#       one can use some(imap(f, seq)) or first(ikeep(f, seq)) for now.

# TODO: vector comparison tests - ascending, descending and such
# def chain_test(compare, seq):
#     return all(compare, izip(seq, rest(seq))

def zipdict(keys, vals):
    return dict(izip(keys, vals))

def flip(mapping):
    def flip_pair(pair):
        k, v = pair
        return v, k
    return walk(flip_pair, mapping)

def project(mapping, keys):
    return _factory(mapping)((k, mapping[k]) for k in keys if k in mapping)

def izip_values(*dicts):
    if len(dicts) < 1:
        raise TypeError('izip_values expects at least one argument')
    keys = set.intersection(*map(set, dicts))
    for key in keys:
        yield tuple(d[key] for d in dicts)

def izip_dicts(*dicts):
    if len(dicts) < 1:
        raise TypeError('izip_dicts expects at least one argument')
    keys = set.intersection(*map(set, dicts))
    for key in keys:
        yield key, tuple(d[key] for d in dicts)


def where(mappings, **cond):
    match = lambda m: all(m[k] == v for k, v in cond.items())
    return filter(match, mappings)

def pluck(key, mappings):
    return map(itemgetter(key), mappings)

def invoke(objects, name, *args, **kwargs):
    return map(methodcaller(name, *args, **kwargs), objects)


if sys.version_info[0] == 3:
    def lwhere(mappings, **cond):
        return list(where(mappings, **cond))

    def lpluck(key, mappings):
        return list(pluck(key, mappings))

    def linvoke(objects, name, *args, **kwargs):
        return list(invoke(objects, name, *args, **kwargs))
