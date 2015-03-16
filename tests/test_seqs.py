from collections import Iterator
from operator import add
import pytest
from whatever import _

from funcy.cross import xrange, PY3
from funcy import is_list
from funcy.seqs import *


def test_repeatedly():
    counter = count()
    c = lambda: next(counter)
    assert take(2, repeatedly(c)) == [0, 1]

def test_iterate():
    assert take(4, iterate(_ * 2, 1)) == [1, 2, 4, 8]


def test_take():
    assert take(2, [3, 2, 1]) == [3, 2]
    assert take(2, count(7)) == [7, 8]

def test_drop():
    dropped = drop(2, [5, 4, 3, 2])
    assert isinstance(dropped, Iterator)
    assert list(dropped) == [3, 2]

    assert take(2, drop(2, count())) == [2, 3]

def test_first():
    assert first('xyz') == 'x'
    assert first(count(7)) == 7
    assert first([]) is None

def test_second():
    assert second('xyz') == 'y'
    assert second(count(7)) == 8
    assert second('x') is None

def test_last():
    assert last('xyz') == 'z'
    assert last(xrange(1, 10)) == 9
    assert last([]) is None
    assert last(x for x in 'xyz') == 'z'

def test_nth():
    assert nth(0, 'xyz') == 'x'
    assert nth(2, 'xyz') == 'z'
    assert nth(3, 'xyz') is None
    assert nth(3, count(7)) == 10

def test_butlast():
    assert list(butlast('xyz')) == ['x', 'y']
    assert list(butlast([])) == []

def test_ilen():
    assert ilen('xyz') == 3
    assert ilen(xrange(10)) == 10


def test_map():
    assert map(_ * 2, [2, 3]) == [4, 6]
    assert map(None, [2, 3]) == [2, 3]
    assert map(r'\d+', ['a2', '13b']) == ['2', '13']
    assert map({'a': 1, 'b': 2}, 'ab') == [1, 2]
    assert map(set([1,2,3]), [0, 1, 2]) == [False, True, True]
    assert map(1, ['abc', '123']) == ['b', '2']
    assert map(slice(2), ['abc', '123']) == ['ab', '12']

@pytest.mark.skipif(PY3, reason="map(None, ...) doesn't work in python 3")
def test_map_multi():
    assert map(None, [1, 2, 3], 'abc') == [(1, 'a'), (2, 'b'), (3, 'c')]

@pytest.mark.skipif(PY3, reason="imap(None, ...) doesn't work in python 3")
def test_imap_strange():
    """
    Demonstrates funcy.imap and itertools.imap have behavior when given None as f.
    """
    assert list(imap(None, 'abc')) == [('a',), ('b',), ('c',)]

def test_filter():
    assert filter(None, [2, 3, 0]) == [2, 3]
    assert filter(r'\d+', ['a2', '13b', 'c']) == ['a2', '13b']
    assert filter(set([1,2,3]), [0, 1, 2, 4, 1]) == [1, 2, 1]

def test_remove():
    assert remove(_ > 3, range(10)) == [0, 1, 2, 3]

def test_keep():
    assert keep(_ % 3, range(5)) == [1, 2, 1]
    assert keep(range(5)) == [1, 2, 3, 4]
    assert keep(mapcat(range, range(4))) == [1, 1, 2]

def test_concat():
    assert concat('ab', 'cd') == list('abcd')
    assert concat() == []

def test_cat():
    assert cat('abcd') == list('abcd')
    assert cat(range(x) for x in range(3)) == [0, 0, 1]

def test_flatten():
    assert flatten([1, [2, 3]]) == [1, 2, 3]
    assert flatten([[1, 2], 3]) == [1, 2, 3]
    assert flatten([(2, 3)]) == [2, 3]
    assert flatten([iter([2, 3])]) == [2, 3]

def test_flatten_follow():
    assert flatten([1, [2, 3]], follow=is_list) == [1, 2, 3]
    assert flatten([1, [(2, 3)]], follow=is_list) == [1, (2, 3)]

def test_mapcat():
    assert mapcat(lambda x: [x, x], 'abc') == list('aabbcc')

def test_interleave():
    assert list(interleave('ab', 'cd')) == list('acbd')
    assert list(interleave('ab_', 'cd')) == list('acbd')

def test_iterpose():
    assert list(interpose('.', 'abc')) == list('a.b.c')


def test_distinct():
    assert distinct('abcbad') == list('abcd')
    assert distinct([{}, {}, {'a': 1}, {'b': 2}], key=len) == [{}, {'a': 1}]
    assert distinct(['ab', 'cb', 'ad'], key=0) == ['ab', 'cb']

# Separate test as split() is not implemented via it.
def test_isplit():
    assert map(list, isplit(_ % 2, range(5))) == [[1, 3], [0, 2, 4]]

def test_split():
    assert split(_ % 2, range(5)) == ([1, 3], [0, 2, 4])
    # This behaviour moved to split_at()
    with pytest.raises(TypeError): split(2, range(5))

def test_split_at():
    assert split_at(2, range(5)) == ([0, 1], [2, 3, 4])

def test_split_at_pred():
    # This behaviour moved to split_by()
    with pytest.raises(ValueError): split_at(_ % 2, range(5))

def test_split_by():
    assert split_by(_ % 2, [1, 2, 3]) == ([1], [2, 3])

def test_group_by():
    assert group_by(_ % 2, range(5)) == {0: [0, 2, 4], 1: [1, 3]}
    assert group_by(r'\d', ['a1', 'b2', 'c1']) == {'1': ['a1', 'c1'], '2': ['b2']}

def test_group_by_keys():
    assert group_by_keys(r'(\d)(\d)', ['12', '23']) == {'1': ['12'], '2': ['12', '23'], '3': ['23']}

def test_count_by():
    assert count_by(_ % 2, range(5)) == {0: 3, 1: 2}
    assert count_by(r'\d', ['a1', 'b2', 'c1']) == {'1': 2, '2': 1}

def test_count_by_is_defaultdict():
    cnts = count_by(len, [])
    assert cnts[1] == 0

def test_partition():
    assert partition(2, range(5)) == [[0, 1], [2, 3]]
    assert partition(2, 1, range(4)) == [[0, 1], [1, 2], [2, 3]]
    # test iters
    assert partition(2, iter(range(5))) == [[0, 1], [2, 3]]
    assert partition(2, xrange(5)) == [[0, 1], [2, 3]]

def test_chunks():
    assert chunks(2, range(5)) == [[0, 1], [2, 3], [4]]
    assert chunks(2, 1, range(4)) == [[0, 1], [1, 2], [2, 3], [3]]
    assert chunks(3, 1, iter(range(3))) == [[0, 1, 2], [1, 2], [2]]

def test_partition_by():
    assert partition_by(lambda x: x == 3, [1,2,3,4,5]) == [[1,2], [3], [4,5]]
    assert partition_by('x', 'abxcd') == [['a', 'b'], ['x'], ['c', 'd']]


def test_with_prev():
    assert list(with_prev(range(3))) == [(0, None), (1, 0), (2, 1)]

def test_with_next():
    assert list(with_next(range(3))) == [(0, 1), (1, 2), (2, None)]

def test_pairwise():
    assert list(pairwise(range(3))) == [(0, 1), (1, 2)]


def test_reductions():
    assert reductions(add, []) == []
    assert reductions(add, [None]) == [None]
    assert reductions(add, [1, 2, 3, 4]) == [1, 3, 6, 10]
    assert reductions(lambda x, y: x + [y], [1,2,3], []) == [[1], [1, 2], [1, 2, 3]]

def test_sums():
    assert sums([]) == []
    assert sums([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert sums([[1],[2],[3]]) == [[1], [1, 2], [1, 2, 3]]

def test_without():
    assert without([]) == []
    assert without([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert without([1, 2, 1, 0, 3, 1, 4], 0, 1) == [2, 3, 4]
