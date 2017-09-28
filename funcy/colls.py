try:
    from __builtin__ import all as _all, any as _any
except ImportError:
    from builtins import all as _all, any as _any
from operator import itemgetter, methodcaller, attrgetter
from collections import Mapping, Set, Iterable, Iterator, defaultdict
from itertools import chain, tee

from .cross import basestring, xrange, izip, map, filter, imap, PY2
from .primitives import EMPTY
from .funcs import partial, compose
from .funcmakers import make_func, make_pred
from .seqs import take, ximap, ifilter


__all__ = ['empty', 'iteritems', 'itervalues',
           'join', 'merge', 'join_with', 'merge_with',
           'walk', 'walk_keys', 'walk_values', 'select', 'select_keys', 'select_values', 'compact',
           'is_distinct', 'all', 'any', 'none', 'one', 'some',
           'zipdict', 'flip', 'project', 'omit', 'izip_values', 'izip_dicts',
           'where', 'pluck', 'pluck_attr', 'invoke', 'iwhere', 'ipluck', 'ipluck_attr', 'iinvoke',
           'get_in', 'set_in', 'update_in']


### Generic ops
FACTORY_REPLACE = {
    type(object.__dict__): dict,
    type({}.keys()): list,
    type({}.values()): list,
    type({}.items()): list,
}

def _factory(coll, mapper=None):
    # Hack for defaultdicts overriden constructor
    if isinstance(coll, defaultdict):
        item_factory = compose(mapper, coll.default_factory) if mapper else coll.default_factory
        return partial(defaultdict, item_factory)
    elif isinstance(coll, Iterator):
        return iter
    elif isinstance(coll, basestring):
        return ''.join
    elif type(coll) in FACTORY_REPLACE:
        return FACTORY_REPLACE[type(coll)]
    else:
        return coll.__class__

def empty(coll):
    """Creates an empty collection of the same type."""
    if isinstance(coll, Iterator):
        return iter([])
    return _factory(coll)()

if PY2:
    def iteritems(coll):
        return coll.iteritems() if hasattr(coll, 'iteritems') else coll

    def itervalues(coll):
        return coll.itervalues() if hasattr(coll, 'itervalues') else coll
else:
    def iteritems(coll):
        return coll.items() if hasattr(coll, 'items') else coll

    def itervalues(coll):
        return coll.values() if hasattr(coll, 'values') else coll

iteritems.__doc__ = "Yields (key, value) pairs of the given collection."
itervalues.__doc__ = "Yields values of the given collection."


def join(colls):
    """Joins several collections of same type into one."""
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
        # NOTE: this could be reduce(concat, ...),
        #       more effective for low count
        return cls(chain.from_iterable(colls))
    else:
        raise TypeError("Don't know how to join %s" % cls.__name__)

def merge(*colls):
    """Merges several collections of same type into one.

    Works with dicts, sets, lists, tuples, iterators and strings.
    For dicts later values take precedence."""
    return join(colls)


def join_with(f, dicts):
    """Joins several dicts, combining values with given function."""
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
        for k, v in iteritems(lists):
            lists[k] = f(v)

    return lists

def merge_with(f, *dicts):
    """Merges several dicts, combining values with given function."""
    return join_with(f, dicts)


def walk(f, coll):
    """Walks the collection transforming its elements with f.
       Same as map, but preserves coll type."""
    return _factory(coll)(ximap(f, iteritems(coll)))

def walk_keys(f, coll):
    """Walks keys of the collection, mapping them with f."""
    f = make_func(f)
    # NOTE: we use this awkward construct instead of lambda to be Python 3 compatible
    def pair_f(pair):
        k, v = pair
        return f(k), v

    return walk(pair_f, coll)

def walk_values(f, coll):
    """Walks values of the collection, mapping them with f."""
    f = make_func(f)
    # NOTE: we use this awkward construct instead of lambda to be Python 3 compatible
    def pair_f(pair):
        k, v = pair
        return k, f(v)

    return _factory(coll, mapper=f)(ximap(pair_f, iteritems(coll)))

# TODO: prewalk, postwalk and friends

def select(pred, coll):
    """Same as filter but preserves coll type."""
    return _factory(coll)(ifilter(pred, iteritems(coll)))

def select_keys(pred, coll):
    """Select part of the collection with keys passing pred."""
    pred = make_pred(pred)
    return select(lambda pair: pred(pair[0]), coll)

def select_values(pred, coll):
    """Select part of the collection with values passing pred."""
    pred = make_pred(pred)
    return select(lambda pair: pred(pair[1]), coll)


def compact(coll):
    """Removes falsy values from the collection."""
    if isinstance(coll, Mapping):
        return select_values(bool, coll)
    else:
        return select(bool, coll)


### Content tests

def is_distinct(coll, key=EMPTY):
    """Checks if all elements in the collection are different."""
    if key is EMPTY:
        return len(coll) == len(set(coll))
    else:
        return len(coll) == len(set(ximap(key, coll)))


def all(pred, seq=EMPTY):
    """Checks if all items in seq pass pred (or are truthy)."""
    if seq is EMPTY:
        return _all(pred)
    return _all(ximap(pred, seq))

def any(pred, seq=EMPTY):
    """Checks if any item in seq passes pred (or is truthy)."""
    if seq is EMPTY:
        return _any(pred)
    return _any(ximap(pred, seq))

def none(pred, seq=EMPTY):
    """"Checks if none of the items in seq pass pred (or are truthy)."""
    return not any(pred, seq)

def one(pred, seq=EMPTY):
    """Checks whether exactly one item in seq passes pred (or is truthy)."""
    if seq is EMPTY:
        return one(bool, pred)
    return len(take(2, ifilter(pred, seq))) == 1

# Not same as in clojure! returns value found not pred(value)
def some(pred, seq=EMPTY):
    """Finds first item in seq passing pred or first that is truthy."""
    if seq is EMPTY:
        return some(bool, pred)
    return next(ifilter(pred, seq), None)

# TODO: a variant of some that returns mapped value,
#       one can use some(imap(f, seq)) or first(ikeep(f, seq)) for now.

# TODO: vector comparison tests - ascending, descending and such
# def chain_test(compare, seq):
#     return all(compare, izip(seq, rest(seq))

def zipdict(keys, vals):
    """Creates a dict with keys mapped to the corresponding vals."""
    return dict(izip(keys, vals))

def flip(mapping):
    """Flip passed dict or collection of pairs swapping its keys and values."""
    def flip_pair(pair):
        k, v = pair
        return v, k
    return walk(flip_pair, mapping)

def project(mapping, keys):
    """Leaves only given keys in mapping."""
    return _factory(mapping)((k, mapping[k]) for k in keys if k in mapping)

def omit(mapping, keys):
    """Removes given keys from mapping."""
    return _factory(mapping)((k, v) for k, v in iteritems(mapping) if k not in keys)

def izip_values(*dicts):
    """Yields tuples of corresponding values of several dicts."""
    if len(dicts) < 1:
        raise TypeError('izip_values expects at least one argument')
    keys = set.intersection(*map(set, dicts))
    for key in keys:
        yield tuple(d[key] for d in dicts)

def izip_dicts(*dicts):
    """Yields tuples like (key, val1, val2, ...)
       for each common key in all given dicts."""
    if len(dicts) < 1:
        raise TypeError('izip_dicts expects at least one argument')
    keys = set.intersection(*map(set, dicts))
    for key in keys:
        yield key, tuple(d[key] for d in dicts)


def get_in(coll, path, default=None):
    """Returns a value at path in the given nested collection."""
    for key in path:
        try:
            coll = coll[key]
        except (KeyError, IndexError):
            return default
    return coll

def set_in(coll, path, value):
    """Creates a copy of coll with the value set at path."""
    return update_in(coll, path, lambda _: value)

def update_in(coll, path, update, default=None):
    """Creates a copy of coll with a value updated at path."""
    if not path:
        return update(coll)
    elif isinstance(coll, list):
        copy = coll[:]
        # NOTE: there is no auto-vivication for lists
        copy[path[0]] = update_in(copy[path[0]], path[1:], update, default)
        return copy
    else:
        copy = coll.copy()
        current_default = {} if len(path) > 1 else default
        copy[path[0]] = update_in(copy.get(path[0], current_default), path[1:], update, default)
        return copy


def where(mappings, **cond):
    """Selects mappings containing all pairs in cond."""
    items = cond.items()
    match = lambda m: all(k in m and m[k] == v for k, v in items)
    return filter(match, mappings)

def pluck(key, mappings):
    """Lists values for key in each mapping."""
    return map(itemgetter(key), mappings)

def pluck_attr(attr, objects):
    """Lists values of given attribute of each object."""
    return map(attrgetter(attr), objects)

def invoke(objects, name, *args, **kwargs):
    """Makes a list of results of the obj.name(*args, **kwargs)
       for each object in objects."""
    return map(methodcaller(name, *args, **kwargs), objects)


# Iterator versions for python 3 interface

def iwhere(mappings, **cond):
    """Iterates over mappings containing all pairs in cond."""
    items = cond.items()
    match = lambda m: all(k in m and m[k] == v for k, v in items)
    return ifilter(match, mappings)

def ipluck(key, mappings):
    """Iterates over values for key in mappings."""
    return imap(itemgetter(key), mappings)

def ipluck_attr(attr, objects):
    """Iterates over values of given attribute of given objects."""
    return imap(attrgetter(attr), objects)

def iinvoke(objects, name, *args, **kwargs):
    """Yields results of the obj.name(*args, **kwargs)
       for each object in objects."""
    return imap(methodcaller(name, *args, **kwargs), objects)
