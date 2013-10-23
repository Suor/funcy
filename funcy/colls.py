from __builtin__ import all as _all, any as _any
from operator import itemgetter, methodcaller
from collections import Mapping, Set, Iterable, Iterator, defaultdict
from itertools import chain, tee

from .primitives import EMPTY
from .funcs import identity, partial, complement
from .funcmakers import wrap_mapper, wrap_selector
from .seqs import take, imap, ifilter


__all__ = ['empty', 'iteritems',
           'join', 'merge',
           'walk', 'walk_keys', 'walk_values', 'select', 'select_keys', 'select_values', 'compact',
           'is_distinct', 'all', 'any', 'none', 'one', 'some',
           'zipdict', 'flip', 'project', 'izip_values', 'izip_dicts',
           'where', 'pluck', 'invoke']


### Generic ops
def _factory(coll):
    # Hack for defaultdicts overriden constructor
    if isinstance(coll, defaultdict):
        return partial(defaultdict, coll.default_factory)
    elif isinstance(coll, Iterator):
        return identity
    elif isinstance(coll, basestring):
        return ''.join
    else:
        return coll.__class__

def empty(coll):
    return _factory(coll)()

def iteritems(coll):
    return coll.iteritems() if hasattr(coll, 'iteritems') else coll


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

@wrap_mapper
def walk_keys(f, coll):
    return walk(lambda (k, v): (f(k), v), coll)

@wrap_mapper
def walk_values(f, coll):
    return walk(lambda (k, v): (k, f(v)), coll)

# TODO: prewalk, postwalk and friends

def select(pred, coll):
    """Same as filter but preserves coll type."""
    return _factory(coll)(ifilter(pred, iteritems(coll)))

@wrap_selector
def select_keys(pred, coll):
    return select(lambda (k, v): pred(k), coll)

@wrap_selector
def select_values(pred, coll):
    return select(lambda (k, v): pred(v), coll)


def compact(coll):
    if isinstance(coll, Mapping):
        return select_values(bool, coll)
    else:
        return select(bool, coll)


### Content tests

def is_distinct(coll):
    return len(coll) == len(set(coll))


def all(pred, seq=EMPTY):
    if seq is EMPTY:
        return _all(pred)
    return _all(imap(pred, seq))

def any(pred, seq=EMPTY):
    if seq is EMPTY:
        return _any(pred)
    return _any(imap(pred, seq))

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
    return dict(zip(keys, vals))

def flip(mapping):
    return walk(lambda (k, v): (v, k), mapping)

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
        yield tuple([key] + [d[key] for d in dicts])


def where(mappings, **cond):
    match = lambda m: all(m[k] == v for k, v in cond.items())
    return filter(match, mappings)

def pluck(key, mappings):
    return map(itemgetter(key), mappings)

def invoke(objects, name, *args, **kwargs):
    return map(methodcaller(name, *args, **kwargs), objects)
