from math import sin, cos
from datetime import timedelta
import pytest

from funcy.calc import *


def test_memoize():
    @memoize
    def inc(x):
        calls.append(x)
        return x + 1

    calls = []
    assert inc(0) == 1
    assert inc(1) == 2
    assert inc(0) == 1
    assert calls == [0, 1]

    # using kwargs
    assert inc(x=0) == 1
    assert inc(x=1) == 2
    assert inc(x=0) == 1
    assert calls == [0, 1, 0, 1]


def test_memoize_args_kwargs():
    @memoize
    def mul(x, by=1):
        calls.append((x, by))
        return x * by

    calls = []
    assert mul(0) == 0
    assert mul(1) == 1
    assert mul(0) == 0
    assert calls == [(0, 1), (1, 1)]

    # more with kwargs
    assert mul(0, 1) == 0
    assert mul(1, 1) == 1
    assert mul(0, 1) == 0
    assert calls == [(0, 1), (1, 1), (0, 1), (1, 1)]


def test_memoize_skip():
    @memoize
    def inc(x):
        calls.append(x)
        if x == 2:
            raise memoize.skip
        if x == 3:
            raise memoize.skip(42)
        return x + 1

    calls = []
    assert inc(1) == 2
    assert inc(2) is None
    assert inc(2) is None
    assert inc(3) == 42
    assert inc(3) == 42
    assert calls == [1, 2, 2, 3, 3]


def test_memoize_memory():
    @memoize
    def inc(x):
        calls.append(x)
        return x + 1

    calls = []
    inc(0)
    inc.memory.clear()
    inc(0)
    assert calls == [0, 0]


def test_memoize_key_func():
    @memoize(key_func=len)
    def inc(s):
        calls.append(s)
        return s * 2

    calls = []
    assert inc('a') == 'aa'
    assert inc('b') == 'aa'
    inc('ab')
    assert calls == ['a', 'ab']


def test_memoize_direct_key_func():
    calls = []

    def total(values):
        calls.append(list(values))
        return sum(values)

    cached_total = memoize(total, key_func=tuple)
    assert cached_total([1, 2]) == 3
    assert cached_total([1, 2]) == 3
    assert calls == [[1, 2]]

    cached_total.invalidate([1, 2])
    assert cached_total([1, 2]) == 3
    assert calls == [[1, 2], [1, 2]]


@pytest.mark.parametrize('deco', [memoize(), cache(60)], ids=['memoize', 'cache'])
def test_reused_memory_decorator(deco):
    calls = []

    @deco
    def inc(x):
        calls.append('inc')
        return x + 1

    @deco
    def double(x):
        calls.append('double')
        return x * 2

    assert inc(3) == 4
    assert double(3) == 6
    assert inc(3) == 4
    assert double(3) == 6
    assert calls == ['inc', 'double']

    inc.invalidate(3)
    assert double(3) == 6
    assert inc(3) == 4
    assert calls == ['inc', 'double', 'inc']

    inc.invalidate_all()
    assert double(3) == 6
    assert inc(3) == 4
    assert calls == ['inc', 'double', 'inc', 'inc']


def test_make_lookuper():
    @make_lookuper
    def letter_index():
        return ((c, i) for i, c in enumerate('abcdefghij'))

    assert letter_index('c') == 2
    with pytest.raises(LookupError): letter_index('_')


def test_make_lookuper_nested():
    tables_built = [0]

    @make_lookuper
    def function_table(f):
        tables_built[0] += 1
        return ((x, f(x)) for x in range(10))

    assert function_table(sin)(5) == sin(5)
    assert function_table(cos)(3) == cos(3)
    assert function_table(sin)(3) == sin(3)
    assert tables_built[0] == 2

    with pytest.raises(LookupError): function_table(cos)(-1)


def test_silent_lookuper():
    @silent_lookuper
    def letter_index():
        return ((c, i) for i, c in enumerate('abcdefghij'))

    assert letter_index('c') == 2
    assert letter_index('_') is None


def test_silnent_lookuper_nested():
    @silent_lookuper
    def function_table(f):
        return ((x, f(x)) for x in range(10))

    assert function_table(sin)(5) == sin(5)
    assert function_table(cos)(-1) is None


@pytest.mark.parametrize('typ',
    [pytest.param(int, id='int'), pytest.param(lambda s: timedelta(seconds=s), id='timedelta')])
def test_cache(typ):
    calls = []

    @cache(timeout=typ(60))
    def inc(x):
        calls.append(x)
        return x + 1

    assert inc(0) == 1
    assert inc(1) == 2
    assert inc(0) == 1
    assert calls == [0, 1]


def test_cache_mixed_args():
    @cache(timeout=60)
    def add(x, y):
        return x + y

    assert add(1, y=2) == 3


def test_cache_timedout():
    calls = []

    @cache(timeout=0)
    def inc(x):
        calls.append(x)
        return x + 1

    assert inc(0) == 1
    assert inc(1) == 2
    assert inc(0) == 1
    assert calls == [0, 1, 0]
    assert len(inc.memory) == 1  # Both call should be erased then one added


def test_cache_expiration_preserves_refilled_key(monkeypatch):
    now = [0]
    monkeypatch.setattr('funcy.calc.time.time', lambda: now[0])
    calls = []

    @cache(10)
    def cached(key):
        calls.append(key)
        return len(calls)

    assert cached('refilled') == 1
    assert cached('expired') == 2
    now[0] = 5
    cached.invalidate('refilled')
    assert cached('refilled') == 3

    now[0] = 10
    assert cached('expired') == 4
    assert cached('refilled') == 3
    assert calls == ['refilled', 'expired', 'refilled', 'expired']

    now[0] = 15
    assert cached('refilled') == 5
    assert cached('expired') == 4


def test_cache_invalidate():
    calls = []

    @cache(timeout=60)
    def inc(x):
        calls.append(x)
        return x + 1

    assert inc(0) == 1
    assert inc(1) == 2
    assert inc(0) == 1
    assert calls == [0, 1]

    inc.invalidate_all()
    assert inc(0) == 1
    assert inc(1) == 2
    assert inc(0) == 1
    assert calls == [0, 1, 0, 1]

    inc.invalidate(1)
    assert inc(0) == 1
    assert inc(1) == 2
    assert inc(0) == 1
    assert calls == [0, 1, 0, 1, 1]

    # ensure invalidate() is idempotent (doesn't raise KeyError on the 2nd call)
    inc.invalidate(0)
    inc.invalidate(0)
