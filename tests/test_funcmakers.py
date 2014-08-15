import inspect
from collections import defaultdict

import pytest
from funcy.funcmakers import *


def test_callable():
    assert make_func(lambda x: x + 42)(0) == 42


def test_int():
    assert make_func(0)('abc') == 'a'
    assert make_func(2)([1,2,3]) == 3
    assert make_func(1)({1: 'a'}) == 'a'
    with pytest.raises(IndexError): make_func(1)('a')
    with pytest.raises(TypeError): make_func(1)(42)


def test_slice():
    assert make_func(slice(1, None))('abc') == 'bc'


def test_str():
    assert make_func('\d+')('ab42c') == '42'
    assert make_func('\d+')('abc') is None
    assert make_pred('\d+')('ab42c') is True
    assert make_pred('\d+')('abc') is False


def test_dict():
    assert make_func({1: 'a'})(1) == 'a'
    with pytest.raises(KeyError): make_func({1: 'a'})(2)

    d = defaultdict(int, a=42)
    assert make_func(d)('a') == 42
    assert make_func(d)('b') == 0


def test_set():
    s = set([1,2,3])
    assert make_func(s)(1) is True
    assert make_func(s)(4) is False


def test_signature():
    @wrap_mapper
    def seq_f(f, seq):
        pass
    assert inspect.getargspec(seq_f).args == ['f', 'seq']

    @wrap_mapper
    def coll_f(f, coll):
        pass
    assert inspect.getargspec(coll_f).args == ['f', 'coll']

    @wrap_selector
    def seqs_f(f, *seqs):
        pass

    spec = inspect.getargspec(seqs_f)
    assert spec.args == ['f']
    assert spec.varargs == 'seqs'
