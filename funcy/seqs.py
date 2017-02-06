from operator import add
from itertools import islice, chain, tee, groupby, \
                      takewhile as _takewhile, dropwhile as _dropwhile
from collections import defaultdict, deque, Sequence

from .cross import map as _map, filter as _filter, ifilter as _ifilter, imap as _imap, \
                   izip, ifilterfalse, xrange, PY2
from .primitives import EMPTY
from .types import is_seqcont
from .funcs import partial
from .funcmakers import make_func, make_pred


__all__ = [
    'count', 'cycle', 'repeat', 'repeatedly', 'iterate',
    'take', 'drop', 'first', 'second', 'nth', 'last', 'rest', 'butlast', 'ilen',
    'map', 'filter', 'imap', 'ifilter', 'remove', 'iremove', 'keep', 'ikeep', 'without', 'iwithout',
    'concat', 'iconcat', 'chain', 'cat', 'icat', 'flatten', 'iflatten', 'mapcat', 'imapcat',
    'izip', 'interleave', 'interpose', 'distinct', 'idistinct',
    'dropwhile', 'takewhile', 'split', 'isplit', 'split_at', 'isplit_at', 'split_by', 'isplit_by',
    'group_by', 'group_by_keys', 'group_values', 'count_by',
    'partition', 'ipartition', 'chunks', 'ichunks', 'ipartition_by', 'partition_by',
    'with_prev', 'with_next', 'pairwise',
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

def nth(n, seq):
    try:
        return seq[n]
    except IndexError:
        return None
    except TypeError:
        return next(islice(seq, n, None), None)

def last(seq):
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
    """
    # NOTE: implementation borrowed from http://stackoverflow.com/a/15112059/753382
    counter = count()
    deque(izip(seq, counter), maxlen=0)  # (consume at C speed)
    return next(counter)


# TODO: tree-seq equivalent

def map(f, *seqs):
    return _map(make_func(f, builtin=PY2), *seqs)

def filter(pred, seq):
    return _filter(make_pred(pred, builtin=PY2), seq)

def imap(f, *seqs):
    return _imap(make_func(f, builtin=PY2), *seqs)

def ifilter(f, *seqs):
    return _ifilter(make_pred(f, builtin=PY2), *seqs)

if PY2:
    # NOTE: Default imap() behaves strange when passed None as function,
    #       returns 1-length tuples, which is inconvinient and incompatible with map().
    #       This version is more sane: map() compatible and suitable for our internal use.
    def ximap(f, *seqs):
        return _imap(make_func(f), *seqs)
else:
    ximap = imap


def remove(pred, seq):
    return list(iremove(pred, seq))

def iremove(pred, seq):
    return ifilterfalse(make_pred(pred, builtin=PY2), seq)

def keep(f, seq=EMPTY):
    if seq is EMPTY:
        return filter(bool, f)
    else:
        return filter(bool, ximap(f, seq))

def ikeep(f, seq=EMPTY):
    if seq is EMPTY:
        return ifilter(bool, f)
    else:
        return ifilter(bool, ximap(f, seq))

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
            for sub in iflatten(item, follow):
                yield sub
        else:
            yield item

def flatten(seq, follow=is_seqcont):
    return list(iflatten(seq, follow))

def mapcat(f, *seqs):
    return cat(ximap(f, *seqs))

def imapcat(f, *seqs):
    return icat(ximap(f, *seqs))

def interleave(*seqs):
    return icat(izip(*seqs))

def interpose(sep, seq):
    return drop(1, interleave(repeat(sep), seq))


def takewhile(pred, seq=EMPTY):
    if seq is EMPTY:
        pred, seq = bool, pred
    else:
        pred = make_pred(pred)
    return _takewhile(pred, seq)

def dropwhile(pred, seq=EMPTY):
    if seq is EMPTY:
        pred, seq = bool, pred
    else:
        pred = make_pred(pred)
    return _dropwhile(pred, seq)


def distinct(seq, key=EMPTY):
    "Order preserving distinct"
    return list(idistinct(seq, key))

def idistinct(seq, key=EMPTY):
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
    pred = make_pred(pred)
    yes, no = [], []
    for item in seq:
        if pred(item):
            yes.append(item)
        else:
            no.append(item)
    return yes, no


def isplit_at(n, seq):
    a, b = tee(seq)
    return islice(a, n), islice(b, n, None)

def split_at(n, seq):
    a, b = isplit_at(n, seq)
    return list(a), list(b)

def isplit_by(pred, seq):
    a, b = tee(seq)
    return takewhile(pred, a), dropwhile(pred, b)

def split_by(pred, seq):
    a, b = isplit_by(pred, seq)
    return list(a), list(b)


def group_by(f, seq):
    f = make_func(f)
    result = defaultdict(list)
    for item in seq:
        result[f(item)].append(item)
    return result

def group_by_keys(get_keys, seq):
    get_keys = make_func(get_keys)
    result = defaultdict(list)
    for item in seq:
        for k in get_keys(item):
            result[k].append(item)
    return result


def group_values(seq):
    result = defaultdict(list)
    for key, value in seq:
        result[key].append(value)
    return result


def count_by(f, seq):
    f = make_func(f)
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
    # NOTE: range() is capable of slicing in python 3,
    #       so this implementation could be updated
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

def ipartition_by(f, seq):
    f = make_func(f)
    for _, items in groupby(seq, f):
        yield items

def partition_by(f, seq):
    return map(list, ipartition_by(f, seq))


def with_prev(seq, fill=None):
    a, b = tee(seq)
    return izip(a, chain([fill], b))

def with_next(seq, fill=None):
    a, b = tee(seq)
    next(b, None)
    return izip(a, chain(b, [fill]))

# An itertools recipe
# NOTE: this is the same as ipartition(2, 1, seq) only faster and with distinct name
def pairwise(seq):
    a, b = tee(seq)
    next(b, None)
    return izip(a, b)


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

def reductions(f, seq, acc=EMPTY):
    return list(ireductions(f, seq, acc))

isums = partial(ireductions, add)
sums = partial(reductions, add)
