"""Sequence helpers for async iterables (Python 3.6+).

Import explicitly with ``from funcy import aio``. Lazy helpers return async
iterators; eager helpers return awaitables. Inputs may be synchronous or async,
and callbacks may return values or awaitables. Work is sequential and lazy:
there is no prefetching, task creation, or implicit closing of borrowed inputs.
Use the input's context manager when it owns resources.
"""
from collections import defaultdict
from inspect import isawaitable
from operator import index

from .funcmakers import make_func, make_pred
from .primitives import EMPTY
from .seqs import _cut_seq


__all__ = [
    'take', 'drop', 'first', 'second', 'nth', 'last', 'rest', 'ilen',
    'map', 'lmap', 'filter', 'lfilter', 'remove', 'lremove', 'keep', 'lkeep',
    'concat', 'lconcat', 'cat', 'lcat', 'mapcat', 'lmapcat',
    'takewhile', 'dropwhile', 'distinct', 'ldistinct', 'group_by', 'count_by',
    'partition', 'lpartition', 'chunks', 'lchunks', 'reductions', 'lreductions',
]


async def _from_iterable(seq):
    for item in seq:
        yield item


def _iter(seq):
    return seq.__aiter__() if hasattr(seq, '__aiter__') else _from_iterable(seq)


def _count(n):
    n = index(n)
    if n < 0:
        raise ValueError('n must be non-negative')
    return n


async def take(n, seq):
    """Return up to n items, leaving the rest of the input unconsumed."""
    n = _count(n)
    it = _iter(seq)
    result = []
    for _ in range(n):
        try:
            item = await it.__anext__()
        except StopAsyncIteration:
            break
        result.append(item)
    return result


def drop(n, seq):
    """Skip n items and yield the rest, with funcy's argument order."""
    return _drop(_count(n), seq)


async def _drop(n, seq):
    it = _iter(seq)
    for _ in range(n):
        try:
            await it.__anext__()
        except StopAsyncIteration:
            return
    async for item in it:
        yield item


async def first(seq):
    items = await take(1, seq)
    return items[0] if items else None


async def second(seq):
    return await nth(1, seq)


async def nth(n, seq):
    """Return the zero-based nth item, or None if it does not exist."""
    try:
        return seq[n]
    except IndexError:
        return None
    except TypeError:
        return await first(drop(n, seq))


async def last(seq):
    item = None
    async for item in _iter(seq):
        pass
    return item


def rest(seq):
    return drop(1, seq)


async def ilen(seq):
    count = 0
    async for _ in _iter(seq):
        count += 1
    return count


def map(f, *seqs):
    """Map a sync/async extended function, stopping at the shortest input."""
    if not seqs:
        raise TypeError('map() requires at least one iterable')
    return _map(make_func(f), seqs)


async def _map(f, seqs):
    if len(seqs) == 1:
        async for item in _iter(seqs[0]):
            result = f(item)
            yield await result if isawaitable(result) else result
    else:
        its = [_iter(seq) for seq in seqs]
        while True:
            args = []
            for it in its:
                try:
                    item = await it.__anext__()
                except StopAsyncIteration:
                    return
                args.append(item)
            result = f(*args)
            yield await result if isawaitable(result) else result


async def lmap(f, *seqs):
    return [item async for item in map(f, *seqs)]


def filter(pred, seq):
    return _filter(make_pred(pred), seq, False)


def remove(pred, seq):
    return _filter(make_pred(pred), seq, True)


async def _filter(pred, seq, invert):
    async for item in _iter(seq):
        result = pred(item)
        keep_item = await result if isawaitable(result) else result
        if bool(keep_item) != invert:
            yield item


async def lfilter(pred, seq):
    return [item async for item in filter(pred, seq)]


async def lremove(pred, seq):
    return [item async for item in remove(pred, seq)]


def keep(f, seq=EMPTY):
    return filter(None, f if seq is EMPTY else map(f, seq))


async def lkeep(f, seq=EMPTY):
    return [item async for item in keep(f, seq)]


async def cat(seqs):
    async for seq in _iter(seqs):
        async for item in _iter(seq):
            yield item


def concat(*seqs):
    return cat(seqs)


async def lcat(seqs):
    return [item async for item in cat(seqs)]


async def lconcat(*seqs):
    return await lcat(seqs)


def mapcat(f, *seqs):
    return cat(map(f, *seqs))


async def lmapcat(f, *seqs):
    return [item async for item in mapcat(f, *seqs)]


def takewhile(pred, seq=EMPTY):
    if seq is EMPTY:
        pred, seq = bool, pred
    return _takewhile(make_pred(pred), seq)


async def _takewhile(pred, seq):
    async for item in _iter(seq):
        result = pred(item)
        if not (await result if isawaitable(result) else result):
            return
        yield item


def dropwhile(pred, seq=EMPTY):
    if seq is EMPTY:
        pred, seq = bool, pred
    return _dropwhile(make_pred(pred), seq)


async def _dropwhile(pred, seq):
    dropping = True
    async for item in _iter(seq):
        if dropping:
            result = pred(item)
            dropping = await result if isawaitable(result) else result
        if not dropping:
            yield item


async def distinct(seq, key=EMPTY):
    f = None if key is EMPTY else make_func(key)
    seen = set()
    async for item in _iter(seq):
        value = f(item) if f is not None else item
        if f is not None and isawaitable(value):
            value = await value
        if value not in seen:
            seen.add(value)
            yield item


async def ldistinct(seq, key=EMPTY):
    return [item async for item in distinct(seq, key)]


async def group_by(f, seq):
    f = make_func(f)
    result = defaultdict(list)
    async for item in _iter(seq):
        key = f(item)
        key = await key if isawaitable(key) else key
        result[key].append(item)
    return result


async def count_by(f, seq):
    f = make_func(f)
    result = defaultdict(int)
    async for item in _iter(seq):
        key = f(item)
        key = await key if isawaitable(key) else key
        result[key] += 1
    return result


def _cut(drop_tail, n, step, seq):
    if seq is EMPTY:
        step, seq = n, step
    n, step = index(n), index(step)
    if n <= 0 or step <= 0:
        raise ValueError('n and step must be positive')
    return _cut_iter(drop_tail, n, step, seq)


async def _cut_iter(drop_tail, n, step, seq):
    it = _iter(seq)
    pool = await take(n, it)
    while len(pool) == n:
        yield pool
        if step < n:
            pool = pool[step:] + await take(step, it)
        else:
            pool = await take(n, drop(step - n, it))
    if not drop_tail:
        for part in _cut_seq(False, n, step, pool):
            yield part


def partition(n, step, seq=EMPTY):
    return _cut(True, n, step, seq)


def chunks(n, step, seq=EMPTY):
    return _cut(False, n, step, seq)


async def lpartition(n, step, seq=EMPTY):
    return [part async for part in partition(n, step, seq)]


async def lchunks(n, step, seq=EMPTY):
    return [part async for part in chunks(n, step, seq)]


async def reductions(f, seq, acc=EMPTY):
    started = acc is not EMPTY
    async for item in _iter(seq):
        if not started:
            acc = item
            started = True
        else:
            result = f(acc, item)
            acc = await result if isawaitable(result) else result
        yield acc


async def lreductions(f, seq, acc=EMPTY):
    return [item async for item in reductions(f, seq, acc)]
