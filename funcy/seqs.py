from operator import add
from itertools import islice, ifilter, imap, izip, chain, tee, ifilterfalse, dropwhile, takewhile, \
                      groupby
from collections import defaultdict, deque, Sequence

from .primitives import EMPTY
from .types import is_seqcont
from .funcs import partial
from .funcmakers import wrap_mapper, wrap_selector


__all__ = [
    'count', 'cycle', 'repeat', 'repeatedly', 'iterate',
    'take', 'drop', 'first', 'second', 'nth', 'last', 'rest', 'butlast', 'ilen',
    'map', 'filter', 'imap', 'ifilter', 'remove', 'iremove', 'keep', 'ikeep', 'without', 'iwithout',
    'concat', 'iconcat', 'chain', 'cat', 'icat', 'flatten', 'iflatten', 'mapcat', 'imapcat',
    'izip', 'interleave', 'interpose', 'distinct',
    'dropwhile', 'takewhile', 'split', 'split_at', 'split_by',
    'group_by', 'count_by',
    'partition', 'ipartition', 'chunks', 'ichunks', 'ipartition_by', 'partition_by',
    'with_prev', 'pairwise',
    'ireductions', 'reductions', 'isums', 'sums',
]


# Re-export
from itertools import count, cycle, repeat

def repeatedly(f, n=EMPTY):
    _repeat = repeat(None) if n is EMPTY else repeat(None, n)
    return (f() for _ in _repeat)

def iterate(f, x):
    while True:
        yield x
        x = f(x)


def take(n, seq):
    return list(islice(seq, n))

def drop(n, seq):
    return islice(seq, n, None)

def first(seq):
    return next(iter(seq), None)

def second(seq):
    return first(rest(seq))

# TODO: decide how negative indexes should work - count from end or just return None?
#       it raises ValueError for now
def nth(n, seq):
    return next(islice(seq, n, n+1), None)

def last(seq):
    if hasattr(seq, '__getslice__'):
        try:
            return seq[-1]
        except IndexError:
            return None

    item = None
    for item in iter(seq):
        pass
    return item

def rest(seq):
    return drop(1, seq)

def butlast(seq):
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
    """
    Consume an iterable not reading it into memory; return the number of items.
    Implementation borrowed from http://stackoverflow.com/a/15112059/753382
    """
    counter = count()
    deque(izip(seq, counter), maxlen=0)  # (consume at C speed)
    return next(counter)


# TODO: tree-seq equivalent

map = wrap_mapper(map)
imap = wrap_mapper(imap)
filter = wrap_selector(filter)
ifilter = wrap_selector(ifilter)

def remove(pred, seq):
    return list(iremove(pred, seq))
iremove = wrap_selector(ifilterfalse)

def keep(f, seq=EMPTY):
    if seq is EMPTY:
        return filter(bool, f)
    else:
        return filter(bool, imap(f, seq))

def ikeep(f, seq=EMPTY):
    if seq is EMPTY:
        return ifilter(bool, f)
    else:
        return ifilter(bool, imap(f, seq))

def iwithout(seq, *items):
    for value in seq:
        if value not in items:
            yield value

def without(seq, *items):
    return list(iwithout(seq, *items))


def concat(*seqs):
    return list(chain(*seqs))
iconcat = chain

def cat(seqs):
    return list(icat(seqs))
icat = chain.from_iterable

def iflatten(seq, follow=is_seqcont):
    for item in seq:
        if follow(item):
            for sub in iflatten(item, is_seqcont):
                yield sub
        else:
            yield item

def flatten(seq, follow=is_seqcont):
    return list(iflatten(seq, follow))

def mapcat(f, *seqs):
    return cat(imap(f, *seqs))

def imapcat(f, *seqs):
    return icat(imap(f, *seqs))

def interleave(*seqs):
    return icat(izip(*seqs))

def interpose(sep, seq):
    return drop(1, interleave(repeat(sep), seq))

dropwhile = wrap_selector(dropwhile)
takewhile = wrap_selector(takewhile)


def distinct(seq):
    "Order preserving distinct"
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def isplit(pred, seq):
    a, b = tee(seq)
    return ifilter(pred, a), iremove(pred, b)

def split(pred, seq):
    return map(list, isplit(pred, seq))

def isplit_at(n, seq):
    a, b = tee(seq)
    return islice(a, n), islice(b, n, None)

def split_at(n, seq):
    return map(list, isplit_at(n, seq))

def isplit_by(pred, seq):
    a, b = tee(seq)
    return takewhile(pred, a), dropwhile(pred, b)

def split_by(pred, seq):
    return map(list, isplit_by(pred, seq))


# NOTE: should I name it cluster? to distinguish from itertools.groupby
#       or just group?
# NOTE: should it return OrderedDict to preserve order of keys not just values?
@wrap_mapper
def group_by(f, seq):
    result = defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
    return result

@wrap_mapper
def count_by(f, seq):
    result = defaultdict(int)
    for item in seq:
        result[f(item)] += 1
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
    if isinstance(seq, Sequence) and not isinstance(seq, xrange):
        return _icut_seq(drop_tail, n, step, seq)
    else:
        return _icut_iter(drop_tail, n, step, seq)

def ipartition(n, step, seq=EMPTY):
    return _icut(True, n, step, seq)

def partition(n, step, seq=EMPTY):
    return list(ipartition(n, step, seq))

def ichunks(n, step, seq=EMPTY):
    return _icut(False, n, step, seq)

def chunks(n, step, seq=EMPTY):
    return list(ichunks(n, step, seq))

@wrap_selector
def ipartition_by(f, seq):
    for g, items in groupby(seq, f):
        yield items

def partition_by(f, seq):
    return map(list, ipartition_by(f, seq))


def with_prev(seq, fill=None):
    a, b = tee(seq)
    return izip(a, chain([fill], b))

# An itertools recipe
# NOTE: this is the same as ipartition(2, 1, seq) only faster and with distinct name
def pairwise(seq):
    a, b = tee(seq)
    next(b, None)
    return izip(a, b)


def ireductions(f, seq, acc=EMPTY):
    it = iter(seq)
    if acc is EMPTY:
        last = next(it)
        yield last
    else:
        last = acc
    for x in it:
        last = f(last, x)
        yield last

def reductions(f, seq, acc=EMPTY):
    return list(ireductions(f, seq, acc))

isums = partial(ireductions, add)
sums = partial(reductions, add)
