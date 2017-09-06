from itertools import islice, chain, tee, groupby, \
                      takewhile as _takewhile, dropwhile as _dropwhile
from collections import defaultdict, deque, Sequence
import operator

from .cross import map as _map, filter as _filter, ifilter as _ifilter, imap as _imap, \
                   izip, ifilterfalse, xrange, PY2, PY3
from .primitives import EMPTY
from .types import is_seqcont
from .funcmakers import make_func, make_pred


__all__ = [
    'count', 'cycle', 'repeat', 'repeatedly', 'iterate',
    'take', 'drop', 'first', 'second', 'nth', 'last', 'rest', 'butlast', 'ilen',
    'map', 'filter', 'imap', 'ifilter', 'remove', 'iremove', 'keep', 'ikeep', 'without', 'iwithout',
    'concat', 'iconcat', 'chain', 'cat', 'icat', 'flatten', 'iflatten', 'mapcat', 'imapcat',
    'izip', 'interleave', 'interpose', 'distinct', 'idistinct',
    'dropwhile', 'takewhile', 'split', 'isplit', 'split_at', 'isplit_at', 'split_by', 'isplit_by',
    'group_by', 'group_by_keys', 'group_values', 'count_by', 'count_reps',
    'partition', 'ipartition', 'chunks', 'ichunks', 'ipartition_by', 'partition_by',
    'with_prev', 'with_next', 'pairwise',
    'ireductions', 'reductions', 'isums', 'sums', 'accumulate',
]


# Re-export
from itertools import count, cycle, repeat

def repeatedly(f, n=EMPTY):
    """Takes a function of no args, presumably with side effects,
       and returns an infinite (or length n) iterator of calls to it."""
    _repeat = repeat(None) if n is EMPTY else repeat(None, n)
    return (f() for _ in _repeat)

def iterate(f, x):
    """Returns an infinite iterator of `x, f(x), f(f(x)), ...`"""
    while True:
        yield x
        x = f(x)


def take(n, seq):
    """Returns a list of first n items in the sequence,
       or all items if there are fewer than n."""
    return list(islice(seq, n))

def drop(n, seq):
    """Skips first n items in the sequence, yields the rest."""
    return islice(seq, n, None)

def first(seq):
    """Returns the first item in the sequence.
       Returns None if the sequence is empty."""
    return next(iter(seq), None)

def second(seq):
    """Returns second item in the sequence.
       Returns None if there are less than two items in it."""
    return first(rest(seq))

def nth(n, seq):
    """Returns nth item in the sequence or None if no such item exists."""
    try:
        return seq[n]
    except IndexError:
        return None
    except TypeError:
        return next(islice(seq, n, None), None)

def last(seq):
    """Returns the last item in the sequence or iterator.
       Returns None if the sequence is empty."""
    try:
        return seq[-1]
    except IndexError:
        return None
    except TypeError:
        item = None
        for item in seq:
            pass
        return item

def rest(seq):
    """Skips first item in the sequence, yields the rest."""
    return drop(1, seq)

def butlast(seq):
    """Iterates over all elements of the sequence but last."""
    it = iter(seq)
    try:
        prev = next(it)
    except StopIteration:
        pass
    else:
        for item in it:
            yield prev
            prev = item

def ilen(seq):
    """Consumes an iterable not reading it into memory
       and returns the number of items."""
    # NOTE: implementation borrowed from http://stackoverflow.com/a/15112059/753382
    counter = count()
    deque(izip(seq, counter), maxlen=0)  # (consume at C speed)
    return next(counter)


# TODO: tree-seq equivalent

# TODO: map/imap signatures???
def map(f, *seqs):
    """An extended version of builtin map().
       Derives a mapper from string, int, slice, dict or set."""
    return _map(make_func(f, builtin=PY2), *seqs)

def filter(pred, seq):
    """An extended version of builtin filter().
       Derives a predicate from string, int, slice, dict or set."""
    return _filter(make_pred(pred, builtin=PY2), seq)

def imap(f, *seqs):
    """An extended version of builtin imap().
       Derives a mapper from string, int, slice, dict or set."""
    return _imap(make_func(f, builtin=PY2), *seqs)

def ifilter(pred, seq):
    """An extended version of builtin ifilter().
       Derives a predicate from string, int, slice, dict or set."""
    return _ifilter(make_pred(pred, builtin=PY2), seq)

if PY2:
    # NOTE: Default imap() behaves strange when passed None as function,
    #       returns 1-length tuples, which is inconvinient and incompatible with map().
    #       This version is more sane: map() compatible and suitable for our internal use.
    def ximap(f, *seqs):
        return _imap(make_func(f), *seqs)
else:
    ximap = imap


def remove(pred, seq):
    """Creates a list if items passing given predicate."""
    return list(iremove(pred, seq))

def iremove(pred, seq):
    """Iterates items passing given predicate."""
    return ifilterfalse(make_pred(pred, builtin=PY2), seq)

def keep(f, seq=EMPTY):
    """Maps seq with f and keeps only truthy results.
       Simply lists truthy values in one argument version."""
    if seq is EMPTY:
        return filter(bool, f)
    else:
        return filter(bool, ximap(f, seq))

def ikeep(f, seq=EMPTY):
    """Maps seq with f and iterates truthy results.
       Simply iterates truthy values in one argument version."""
    if seq is EMPTY:
        return ifilter(bool, f)
    else:
        return ifilter(bool, ximap(f, seq))

def iwithout(seq, *items):
    """Iterates over sequence skipping items."""
    for value in seq:
        if value not in items:
            yield value

def without(seq, *items):
    """Removes items from sequence, preserves order."""
    return list(iwithout(seq, *items))


def concat(*seqs):
    """Concatenates several sequences."""
    return list(chain(*seqs))
iconcat = chain

def cat(seqs):
    """Concatenates the sequence of sequences."""
    return list(icat(seqs))
icat = chain.from_iterable

def iflatten(seq, follow=is_seqcont):
    """Flattens arbitrary nested sequence.
       Unpacks an item if follow(item) is truthy."""
    for item in seq:
        if follow(item):
            # TODO: use `yield from` when Python 2 is dropped ;)
            for sub in iflatten(item, follow):
                yield sub
        else:
            yield item

def flatten(seq, follow=is_seqcont):
    """Iterates over arbitrary nested sequence.
       Dives into when follow(item) is truthy."""
    return list(iflatten(seq, follow))

def mapcat(f, *seqs):
    """Maps given sequence(s) and concatenates the results."""
    return cat(ximap(f, *seqs))

def imapcat(f, *seqs):
    """Maps given sequence(s) and chains the results."""
    return icat(ximap(f, *seqs))

def interleave(*seqs):
    """Yields first item of each sequence, then second one and so on."""
    return icat(izip(*seqs))

def interpose(sep, seq):
    """Yields items of the sequence alternating with sep."""
    return drop(1, interleave(repeat(sep), seq))

def takewhile(pred, seq=EMPTY):
    """Yields sequence items until first predicate fail.
       Stops on first falsy value in one argument version."""
    if seq is EMPTY:
        pred, seq = bool, pred
    else:
        pred = make_pred(pred)
    return _takewhile(pred, seq)

def dropwhile(pred, seq=EMPTY):
    """Skips the start of the sequence passing pred (or just truthy),
       then iterates over the rest."""
    if seq is EMPTY:
        pred, seq = bool, pred
    else:
        pred = make_pred(pred)
    return _dropwhile(pred, seq)


def distinct(seq, key=EMPTY):
    """Removes duplicates from sequences, preserves order."""
    return list(idistinct(seq, key))

def idistinct(seq, key=EMPTY):
    """Iterates over sequence skipping duplicates"""
    seen = set()
    # check if key is supplied out of loop for efficiency
    if key is EMPTY:
        for item in seq:
            if item not in seen:
                seen.add(item)
                yield item
    else:
        key = make_func(key)
        for item in seq:
            k = key(item)
            if k not in seen:
                seen.add(k)
                yield item


def isplit(pred, seq):
    """Lazily splits items which pass the predicate from the ones that don't.
       Returns a pair (passed, failed) of respective iterators."""
    pred = make_pred(pred)
    yes, no = deque(), deque()
    splitter = (yes.append(item) if pred(item) else no.append(item) for item in seq)

    def _isplit(q):
        while True:
            while q:
                yield q.popleft()
            try:
                next(splitter)
            except StopIteration:
                return

    return _isplit(yes), _isplit(no)

def split(pred, seq):
    """Splits items which pass the predicate from the ones that don't.
       Returns a pair (passed, failed) of respective lists."""
    pred = make_pred(pred)
    yes, no = [], []
    for item in seq:
        if pred(item):
            yes.append(item)
        else:
            no.append(item)
    return yes, no


def isplit_at(n, seq):
    """Lazily splits the sequence at given position,
       returning a pair of iterators over its start and tail."""
    a, b = tee(seq)
    return islice(a, n), islice(b, n, None)

def split_at(n, seq):
    """Splits the sequence at given position,
       returning a tuple of its start and tail."""
    a, b = isplit_at(n, seq)
    return list(a), list(b)

def isplit_by(pred, seq):
    """Lazily splits the start of the sequence,
       consisting of items passing pred, from the rest of it."""
    a, b = tee(seq)
    return takewhile(pred, a), dropwhile(pred, b)

def split_by(pred, seq):
    """Splits the start of the sequence,
       consisting of items passing pred, from the rest of it."""
    a, b = isplit_by(pred, seq)
    return list(a), list(b)


def group_by(f, seq):
    """Groups given sequence items into a mapping f(item) -> [item, ...]."""
    f = make_func(f)
    result = defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
    return result

def group_by_keys(get_keys, seq):
    """Groups items having multiple keys into a mapping key -> [item, ...].
       Item might be repeated under several keys."""
    get_keys = make_func(get_keys)
    result = defaultdict(list)
    for item in seq:
        for k in get_keys(item):
            result[k].append(item)
    return result


def group_values(seq):
    """Takes a sequence of (key, value) pairs and groups values by keys."""
    result = defaultdict(list)
    for key, value in seq:
        result[key].append(value)
    return result


def count_by(f, seq):
    """Counts numbers of occurrences of values of f()
       on elements of given sequence."""
    f = make_func(f)
    result = defaultdict(int)
    for item in seq:
        result[f(item)] += 1
    return result


def count_reps(seq):
    """Counts number occurrences of each value in the sequence."""
    result = defaultdict(int)
    for item in seq:
        result[item] += 1
    return result


# For efficiency we use separate implementation for cutting sequences (those capable of slicing)
def _icut_seq(drop_tail, n, step, seq):
    limit = len(seq)-n+1 if drop_tail else len(seq)
    return (seq[i:i+n] for i in xrange(0, limit, step))

def _icut_iter(drop_tail, n, step, seq):
    it = iter(seq)
    pool = take(n, it)
    while True:
        if len(pool) < n:
            break
        yield pool
        pool = pool[step:]
        pool.extend(islice(it, step))
    if not drop_tail:
        for item in _icut_seq(drop_tail, n, step, pool):
            yield item

def _icut(drop_tail, n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step
    # NOTE: range() is capable of slicing in python 3,
    if isinstance(seq, Sequence) and (PY3 or not isinstance(seq, xrange)):
        return _icut_seq(drop_tail, n, step, seq)
    else:
        return _icut_iter(drop_tail, n, step, seq)

def ipartition(n, step, seq=EMPTY):
    """Lazily partitions seq into parts of length n.
       Skips step items between parts if passed. Non-fitting tail is ignored."""
    return _icut(True, n, step, seq)

def partition(n, step, seq=EMPTY):
    """Partitions seq into parts of length n.
       Skips step items between parts if passed. Non-fitting tail is ignored."""
    return list(ipartition(n, step, seq))

def ichunks(n, step, seq=EMPTY):
    """Lazily chunks seq into parts of length n or less.
       Skips step items between parts if passed."""
    return _icut(False, n, step, seq)

def chunks(n, step, seq=EMPTY):
    """Chunks seq into parts of length n or less.
       Skips step items between parts if passed."""
    return list(ichunks(n, step, seq))

def ipartition_by(f, seq):
    """Lazily partition seq into continuous chunks with constant value of f."""
    f = make_func(f)
    for _, items in groupby(seq, f):
        yield items

def partition_by(f, seq):
    """Partition seq into continuous chunks with constant value of f."""
    return map(list, ipartition_by(f, seq))


def with_prev(seq, fill=None):
    """Yields each item paired with its preceding: (item, prev)."""
    a, b = tee(seq)
    return izip(a, chain([fill], b))

def with_next(seq, fill=None):
    """Yields each item paired with its following: (item, next)."""
    a, b = tee(seq)
    next(b, None)
    return izip(a, chain(b, [fill]))

# An itertools recipe
# NOTE: this is the same as ipartition(2, 1, seq) only faster and with distinct name
def pairwise(seq):
    """Yields all pairs of neighboring items in seq."""
    a, b = tee(seq)
    next(b, None)
    return izip(a, b)


# Use accumulate from itertools if available
try:
    from itertools import accumulate

    def _ireductions(f, seq, acc):
        last = acc
        for x in seq:
            last = f(last, x)
            yield last

    def ireductions(f, seq, acc=EMPTY):
        if acc is EMPTY:
            return accumulate(seq) if f is operator.add else accumulate(seq, f)
        return _ireductions(f, seq, acc)

except ImportError:
    def ireductions(f, seq, acc=EMPTY):
        it = iter(seq)
        if acc is EMPTY:
            try:
                last = next(it)
            except StopIteration:
                return
            yield last
        else:
            last = acc
        for x in it:
            last = f(last, x)
            yield last

    def accumulate(iterable, func=operator.add):
        """Return series of accumulated sums (or other binary function results)."""
        return ireductions(func, iterable)

ireductions.__doc__ = """Yields intermediate reductions of seq by f."""

def reductions(f, seq, acc=EMPTY):
    """Lists intermediate reductions of seq by f."""
    return list(ireductions(f, seq, acc))

def isums(seq, acc=EMPTY):
    """Yields partial sums of seq."""
    return ireductions(operator.add, seq, acc)

def sums(seq, acc=EMPTY):
    """Lists partial sums of seq."""
    return reductions(operator.add, seq, acc)
