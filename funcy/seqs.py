from itertools import islice, ifilter, imap, izip, chain, tee, ifilterfalse
from collections import defaultdict

from .funcs import complement


__all__ = ['count', 'cycle', 'repeat', 'repeatedly', 'iterate',
           'take', 'drop', 'first', 'second', 'rest',
           'imap', 'ifilter', 'remove', 'iremove', 'keep', 'ikeep',
           'concat', 'iconcat', 'cat', 'icat', 'mapcat', 'imapcat',
           'izip', 'interleave', 'interpose', 'distinct',
           'dropwhile', 'takewhile', 'split', 'split_at', 'split_by',
           'group_by', 'partition', 'chunks']


from itertools import count, cycle, repeat

def repeatedly(f, n=None):
    _repeat = repeat(None, n) if n else repeat(None)
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


# TODO: tree-seq equivalent

def remove(pred, seq):
    return list(iremove(pred, seq))
iremove = ifilterfalse

def keep(f, seq=None):
    if seq is None:
        return filter(bool, f)
    else:
        return filter(bool, imap(f, seq))

def ikeep(f, seq=None):
    if seq is None:
        return ifilter(bool, f)
    else:
        return ifilter(bool, imap(f, seq))

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


# Re-export
from itertools import dropwhile, takewhile

def distinct(seq):
    "Order preserving distinct"
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def isplit(pred, seq):
    a, b = tee(seq)
    return ifilter(pred, a), ifilterfalse(pred, b)

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

def partition(n, step, seq=None):
    if seq is None:
        return partition(n, n, step)
    return [seq[i:i+n] for i in xrange(0, len(seq)-n+1, step)]

def chunks(n, step, seq=None):
    if seq is None:
        return chunks(n, n, step)
    return [seq[i:i+n] for i in xrange(0, len(seq), step)]

