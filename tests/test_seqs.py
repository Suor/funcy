from collections.abc import Iterator
from operator import add
import pytest
from whatever import _

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
    assert last(range(1, 10)) == 9
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
    assert ilen(range(10)) == 10


def test_lmap():
    assert lmap(_ * 2, [2, 3]) == [4, 6]
    assert lmap(None, [2, 3]) == [2, 3]
    assert lmap(_ + _, [1, 2], [4, 5]) == [5, 7]

    assert lmap(r'\d+', ['a2', '13b']) == ['2', '13']
    assert lmap({'a': 1, 'b': 2}, 'ab') == [1, 2]
    assert lmap(set([1,2,3]), [0, 1, 2]) == [False, True, True]
    assert lmap(1, ['abc', '123']) == ['b', '2']
    assert lmap(slice(2), ['abc', '123']) == ['ab', '12']


def test_filter():
    assert lfilter(None, [2, 3, 0]) == [2, 3]
    assert lfilter(r'\d+', ['a2', '13b', 'c']) == ['a2', '13b']
    assert lfilter(set([1,2,3]), [0, 1, 2, 4, 1]) == [1, 2, 1]

def test_remove():
    assert lremove(_ > 3, range(10)) == [0, 1, 2, 3]
    assert lremove('^a', ['a', 'b', 'ba']) == ['b', 'ba']

def test_keep():
    assert lkeep(_ % 3, range(5)) == [1, 2, 1]
    assert lkeep(range(5)) == [1, 2, 3, 4]
    assert lkeep(mapcat(range, range(4))) == [1, 1, 2]

def test_concat():
    assert lconcat('ab', 'cd') == list('abcd')
    assert lconcat() == []

def test_cat():
    assert lcat('abcd') == list('abcd')
    assert lcat(range(x) for x in range(3)) == [0, 0, 1]

def test_flatten():
    assert lflatten([1, [2, 3]]) == [1, 2, 3]
    assert lflatten([[1, 2], 3]) == [1, 2, 3]
    assert lflatten([(2, 3)]) == [2, 3]
    assert lflatten([iter([2, 3])]) == [2, 3]

def test_flatten_follow():
    assert lflatten([1, [2, 3]], follow=is_list) == [1, 2, 3]
    assert lflatten([1, [(2, 3)]], follow=is_list) == [1, (2, 3)]

def test_mapcat():
    assert lmapcat(lambda x: [x, x], 'abc') == list('aabbcc')

def test_interleave():
    assert list(interleave('ab', 'cd')) == list('acbd')
    assert list(interleave('ab_', 'cd')) == list('acbd')

def test_iterpose():
    assert list(interpose('.', 'abc')) == list('a.b.c')


def test_takewhile():
    assert list(takewhile([1, 2, None, 3])) == [1, 2]


def test_distinct():
    assert ldistinct('abcbad') == list('abcd')
    assert ldistinct([{}, {}, {'a': 1}, {'b': 2}], key=len) == [{}, {'a': 1}]
    assert ldistinct(['ab', 'cb', 'ad'], key=0) == ['ab', 'cb']

# Separate test as lsplit() is not implemented via it.
def test_split():
    assert lmap(list, split(_ % 2, range(5))) == [[1, 3], [0, 2, 4]]

def test_lsplit():
    assert lsplit(_ % 2, range(5)) == ([1, 3], [0, 2, 4])
    # This behaviour moved to split_at()
    with pytest.raises(TypeError): lsplit(2, range(5))

def test_split_at():
    assert lsplit_at(2, range(5)) == ([0, 1], [2, 3, 4])

def test_split_by():
    assert lsplit_by(_ % 2, [1, 2, 3]) == ([1], [2, 3])

def test_group_by():
    assert group_by(_ % 2, range(5)) == {0: [0, 2, 4], 1: [1, 3]}
    assert group_by(r'\d', ['a1', 'b2', 'c1']) == {'1': ['a1', 'c1'], '2': ['b2']}

def test_group_by_keys():
    assert group_by_keys(r'(\d)(\d)', ['12', '23']) == {'1': ['12'], '2': ['12', '23'], '3': ['23']}

def test_group_values():
    assert group_values(['ab', 'ac', 'ba']) == {'a': ['b', 'c'], 'b': ['a']}

def test_count_by():
    assert count_by(_ % 2, range(5)) == {0: 3, 1: 2}
    assert count_by(r'\d', ['a1', 'b2', 'c1']) == {'1': 2, '2': 1}

def test_count_by_is_defaultdict():
    cnts = count_by(len, [])
    assert cnts[1] == 0

def test_count_reps():
    assert count_reps([0, 1, 0]) == {0: 2, 1: 1}

def test_partition():
    assert lpartition(2, [0, 1, 2, 3, 4]) == [[0, 1], [2, 3]]
    assert lpartition(2, 1, [0, 1, 2, 3]) == [[0, 1], [1, 2], [2, 3]]
    # test iters
    assert lpartition(2, iter(range(5))) == [[0, 1], [2, 3]]
    assert lmap(list, lpartition(2, range(5))) == [[0, 1], [2, 3]]

def test_chunks():
    assert lchunks(2, [0, 1, 2, 3, 4]) == [[0, 1], [2, 3], [4]]
    assert lchunks(2, 1, [0, 1, 2, 3]) == [[0, 1], [1, 2], [2, 3], [3]]
    assert lchunks(3, 1, iter(range(3))) == [[0, 1, 2], [1, 2], [2]]

def test_partition_by():
    assert lpartition_by(lambda x: x == 3, [1,2,3,4,5]) == [[1,2], [3], [4,5]]
    assert lpartition_by('x', 'abxcd') == [['a', 'b'], ['x'], ['c', 'd']]
    assert lpartition_by(r'\d', '1211') == [['1'], ['2'], ['1','1']]


def test_with_prev():
    assert list(with_prev(range(3))) == [(0, None), (1, 0), (2, 1)]

def test_with_next():
    assert list(with_next(range(3))) == [(0, 1), (1, 2), (2, None)]

def test_pairwise():
    assert list(pairwise(range(3))) == [(0, 1), (1, 2)]

def test_lzip():
    assert lzip('12', 'xy') == [('1', 'x'), ('2', 'y')]
    assert lzip('123', 'xy') == [('1', 'x'), ('2', 'y')]
    assert lzip('12', 'xyz') == [('1', 'x'), ('2', 'y')]
    assert lzip('12', iter('xyz')) == [('1', 'x'), ('2', 'y')]

def test_lzip_strict():
    assert lzip('123', 'xy', strict=False) == [('1', 'x'), ('2', 'y')]
    assert lzip('12', 'xy', strict=True) == [('1', 'x'), ('2', 'y')]
    assert lzip('12', iter('xy'), strict=True) == [('1', 'x'), ('2', 'y')]
    for wrap in (str, iter):
        with pytest.raises(ValueError): lzip(wrap('123'), wrap('xy'), strict=True)
        with pytest.raises(ValueError): lzip(wrap('12'), wrap('xyz'), wrap('abcd'), strict=True)
        with pytest.raises(ValueError): lzip(wrap('123'), wrap('xy'), wrap('abcd'), strict=True)
        with pytest.raises(ValueError): lzip(wrap('123'), wrap('xyz'), wrap('ab'), strict=True)


def test_reductions():
    assert lreductions(add, []) == []
    assert lreductions(add, [None]) == [None]
    assert lreductions(add, [1, 2, 3, 4]) == [1, 3, 6, 10]
    assert lreductions(lambda x, y: x + [y], [1,2,3], []) == [[1], [1, 2], [1, 2, 3]]

def test_sums():
    assert lsums([]) == []
    assert lsums([1, 2, 3, 4]) == [1, 3, 6, 10]
    assert lsums([[1],[2],[3]]) == [[1], [1, 2], [1, 2, 3]]

def test_without():
    assert lwithout([]) == []
    assert lwithout([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert lwithout([1, 2, 1, 0, 3, 1, 4], 0, 1) == [2, 3, 4]
