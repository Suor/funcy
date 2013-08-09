from operator import add
from itertools import islice, ifilter, imap, izip, chain, tee, ifilterfalse, dropwhile, takewhile
from collections import defaultdict, Sequence

from .funcs import partial
from .funcmakers import wrap_mapper, wrap_selector


__all__ = [
    'count', 'cycle', 'repeat', 'repeatedly', 'iterate',
    'take', 'drop', 'first', 'second', 'rest', 'ilen',
    'map', 'filter', 'imap', 'ifilter', 'remove', 'iremove', 'keep', 'ikeep', 'without', 'iwithout',
    'concat', 'iconcat', 'chain', 'cat', 'icat', 'mapcat', 'imapcat',
    'izip', 'interleave', 'interpose', 'distinct',
    'dropwhile', 'takewhile', 'split', 'split_at', 'split_by',
    'group_by', 'partition', 'ipartition', 'chunks', 'ichunks', 'with_prev',
    'ireductions', 'reductions', 'isums', 'sums',
]


EMPTY = object() # Used as default for optional arguments


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

def rest(seq):
    return drop(1, seq)

def ilen(seq):
    return sum(1 for _ in seq)


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
        if not value in items:
            yield value

def without(seq, *items):
    return list(iwithout(seq, *items))


def concat(*seqs):
    return list(chain(*seqs))
iconcat = chain

def cat(seqs):
    return list(icat(seqs))
icat = chain.from_iterable

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
def group_by(f, seq):
    result = defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
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
    if isinstance(seq, Sequence):
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


def with_prev(seq):
    a, b = tee(seq)
    return izip(a, chain([None], b))


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
