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
