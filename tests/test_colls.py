import pytest
from itertools import chain, count
from collections import defaultdict, namedtuple
from whatever import _

from funcy.compat import Iterator
from funcy.colls import *


# Utilities
def eq(a, b):
    return type(a) is type(b) and a == b \
       and (a.default_factory == b.default_factory if isinstance(a, defaultdict) else True)

def inc(x):
    return x + 1

def hinc(xs):
    return map(inc, xs)


def test_empty():
    assert eq(empty({'a': 1}), {})
    assert eq(empty(defaultdict(int)), defaultdict(int))
    assert empty(defaultdict(int)).default_factory == defaultdict(int).default_factory

def test_empty_iter():
    it = empty(iter([]))
    assert isinstance(it, Iterator)
    assert list(it) == []

def test_empty_quirks():
    class A:
        FLAG = 1
    assert empty(A.__dict__) == {}
    assert empty({}.keys()) == []
    assert empty({}.values()) == []
    assert empty({}.items()) == []


def test_iteritems():
    assert list(iteritems([1,2])) == [1,2]
    assert list(iteritems((1,2))) == [1,2]
    assert list(iteritems({'a': 1})) == [('a', 1)]

def test_itervalues():
    assert list(itervalues([1,2])) == [1,2]
    assert list(itervalues((1,2))) == [1,2]
    assert list(itervalues({'a': 1})) == [1]


def test_merge():
    assert eq(merge({1: 2}, {3: 4}), {1: 2, 3: 4})

def test_join():
    assert join([]) is None
    with pytest.raises(TypeError): join([1])
    assert eq(join(['ab', '', 'cd']), 'abcd')
    assert eq(join([['a', 'b'], 'c']), list('abc'))
    assert eq(join([('a', 'b'), ('c',)]), tuple('abc'))
    assert eq(join([{'a': 1}, {'b': 2}]), {'a': 1, 'b': 2})
    assert eq(join([{'a': 1}, {'a': 2}]), {'a': 2})
    assert eq(join([{1,2}, {3}]), {1,2,3})

    it1 = (x for x in range(2))
    it2 = (x for x in range(5, 7))
    joined = join([it1, it2])
    assert isinstance(joined, Iterator) and list(joined) == [0,1,5,6]

    dd1 = defaultdict(int, a=1)
    dd2 = defaultdict(int, b=2)
    assert eq(join([dd1, dd2]), defaultdict(int, a=1, b=2))

def test_join_iter():
    assert join(iter('abc')) == 'abc'
    assert join(iter([[1], [2]])) == [1, 2]
    assert eq(join(iter([{'a': 1}, {'b': 2}])), {'a': 1, 'b': 2})
    assert eq(join(iter([{1,2}, {3}])), {1,2,3})

    it1 = (x for x in range(2))
    it2 = (x for x in range(5, 7))
    chained = join(iter([it1, it2]))
    assert isinstance(chained, Iterator) and list(chained) == [0,1,5,6]


def test_merge_with():
    assert merge_with(list, {1: 1}, {1: 10, 2: 2}) == {1: [1, 10], 2: [2]}
    assert merge_with(sum, {1: 1}, {1: 10, 2: 2}) == {1: 11, 2: 2}
    # Also works for collection of pairs
    assert merge_with(sum, {1: 1}, {1: 10, 2: 2}.items()) == {1: 11, 2: 2}

def test_join_with():
    assert join_with(sum, ({n % 3: n} for n in range(5))) == {0: 3, 1: 5, 2: 2}


def test_walk():
    assert eq(walk(inc, [1,2,3]), [2,3,4])
    assert eq(walk(inc, (1,2,3)), (2,3,4))
    assert eq(walk(inc, {1,2,3}), {2,3,4})
    assert eq(walk(hinc, {1:1,2:2,3:3}), {2:2,3:3,4:4})

def test_walk_iter():
    it = walk(inc, chain([0], [1, 2]))
    assert isinstance(it, Iterator) and list(it) == [1,2,3]

    it = walk(inc, (i for i in [0,1,2]))
    assert isinstance(it, Iterator) and list(it) == [1,2,3]

def test_walk_extended():
    assert walk(None, {2, 3}) == {2, 3}
    assert walk(r'\d+', {'a2', '13b'}) == {'2', '13'}
    assert walk({'a': '1', 'b': '2'}, 'ab') == '12'
    assert walk({1, 2, 3}, (0, 1, 2)) == (False, True, True)

def test_walk_keys():
    assert walk_keys(str.upper, {'a': 1, 'b':2}) == {'A': 1, 'B': 2}
    assert walk_keys(r'\d', {'a1': 1, 'b2': 2}) == {'1': 1, '2': 2}

def test_walk_values():
    assert walk_values(_ * 2, {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}
    assert walk_values(r'\d', {1: 'a1', 2: 'b2'}) == {1: '1', 2: '2'}

def test_walk_values_defaultdict():
    dd = defaultdict(lambda: 'hey', {1: 'a', 2: 'ab'})
    walked_dd = walk_values(len, dd)
    assert walked_dd == {1: 1, 2: 2}
    # resulting default factory should be compose(len, lambda: 'hey')
    assert walked_dd[0] == 3


def test_select():
    assert eq(select(_ > 1, [1,2,3]), [2,3])
    assert eq(select(_ > 1, (1,2,3)), (2,3))
    assert eq(select(_ > 1, {1,2,3}), {2,3})
    assert eq(select(_[1] > 1, {'a':1,'b':2,'c':3}), {'b':2,'c':3})
    assert select(_[1] > 1, defaultdict(int)) == {}

def test_select_extended():
    assert select(None, [2, 3, 0]) == [2, 3]
    assert select(r'\d', 'a23bn45') == '2345'
    assert select({1,2,3}, (0, 1, 2, 4, 1)) == (1, 2, 1)

def test_select_keys():
    assert select_keys(_[0] == 'a', {'a':1, 'b':2, 'ab':3}) == {'a': 1, 'ab':3}
    assert select_keys(r'^a', {'a':1, 'b':2, 'ab':3, 'ba': 4}) == {'a': 1, 'ab':3}

def test_select_values():
    assert select_values(_ % 2, {'a': 1, 'b': 2}) == {'a': 1}
    assert select_values(r'a', {1: 'a', 2: 'b'}) == {1: 'a'}


def test_compact():
    assert eq(compact([0, 1, None, 3]), [1, 3])
    assert eq(compact((0, 1, None, 3)), (1, 3))
    assert eq(compact({'a': None, 'b': 0, 'c': 1}), {'c': 1})


def test_is_distinct():
    assert is_distinct('abc')
    assert not is_distinct('aba')
    assert is_distinct(['a', 'ab', 'abc'], key=len)
    assert not is_distinct(['ab', 'cb', 'ad'], key=0)


def test_all():
    assert all([1,2,3])
    assert not all([1,2,''])
    assert all(callable, [abs, open, int])
    assert not all(_ < 3, [1,2,5])

def test_all_extended():
    assert all(None, [1,2,3])
    assert not all(None, [1,2,''])
    assert all(r'\d', '125')
    assert not all(r'\d', '12.5')

def test_any():
    assert any([0, False, 3, ''])
    assert not any([0, False, ''])
    assert any(_ > 0, [1,2,0])
    assert not any(_ < 0, [1,2,0])

def test_one():
    assert one([0, False, 3, ''])
    assert not one([0, False, ''])
    assert not one([1, False, 'a'])
    assert one(_ > 0, [0,1])
    assert not one(_ < 0, [0,1,2])
    assert not one(_ > 0, [0,1,2])

def test_none():
    assert none([0, False])
    assert not none(_ < 0, [0, -1])

def test_some():
    assert some([0, '', 2, 3]) == 2
    assert some(_ > 3, range(10)) == 4


def test_zipdict():
    assert zipdict([1, 2], 'ab') == {1: 'a', 2:'b'}
    assert zipdict('ab', count()) == {'a': 0, 'b': 1}

def test_flip():
    assert flip({'a':1, 'b':2}) == {1:'a', 2:'b'}

def test_project():
    assert project({'a':1, 'b':2, 'c': 3}, 'ac') == {'a':1, 'c': 3}
    dd = defaultdict(int, {'a':1, 'b':2, 'c': 3})
    assert eq(project(dd, 'ac'), defaultdict(int, {'a':1, 'c': 3}))

def test_omit():
    assert omit({'a': 1, 'b': 2, 'c': 3}, 'ac') == {'b': 2}
    dd = defaultdict(int, {'a': 1, 'b': 2, 'c': 3})
    assert eq(omit(dd, 'ac'), defaultdict(int, {'b': 2}))

def test_zip_values():
    assert list(zip_values({1: 10}, {1: 20, 2: 30})) == [(10, 20)]
    with pytest.raises(TypeError): list(zip_values())

def test_zip_dicts():
    assert list(zip_dicts({1: 10}, {1: 20, 2: 30})) == [(1, (10, 20))]
    with pytest.raises(TypeError): list(zip_dicts())


def test_get_in():
    d = {
        "a": {
            "b": "c",
            "d": "e",
            "f": {
                "g": "h"
            }
        },
        "i": "j"
    }
    assert get_in(d, ["m"]) is None
    assert get_in(d, ["m", "n"], "foo") == "foo"
    assert get_in(d, ["i"]) == "j"
    assert get_in(d, ["a", "b"]) == "c"
    assert get_in(d, ["a", "f", "g"]) == "h"

def test_get_in_list():
    assert get_in([1, 2], [0]) == 1
    assert get_in([1, 2], [3]) is None
    assert get_in({'x': [1, 2]}, ['x', 1]) == 2

def test_set_in():
    d = {
        'a': {
            'b': 1,
            'c': 2,
        },
        'd': 5
    }

    d2 = set_in(d, ['a', 'c'], 7)
    assert d['a']['c'] == 2
    assert d2['a']['c'] == 7

    d3 = set_in(d, ['e', 'f'], 42)
    assert d3['e'] == {'f': 42}
    assert d3['a'] is d['a']

def test_set_in_list():
    l = [{}, 1]
    l2 = set_in(l, [1], 7)
    assert l2 == [{}, 7]
    assert l2[0] is l[0]

def test_update_in():
    d = {'c': []}

    assert update_in(d, ['c'], len) == {'c': 0}

    d2 = update_in(d, ['a', 'b'], inc, default=0)
    assert d2['a']['b'] == 1
    assert d2['c'] is d['c']

def test_del_in():
    d = {'c': [1, 2, 3]}

    assert del_in(d, []) is d
    assert del_in(d, ['a', 'b']) is d
    assert del_in(d, ['c', 1]) == {'c': [1, 3]}
    with pytest.raises(TypeError): del_in(d, ['c', 'b'])

def test_has_path():
    d = {
        "a": {
            "b": "c",
            "d": "e",
            "f": {
                "g": "h"
            }
        },
        "i": "j"
    }

    assert has_path(d, [])
    assert not has_path(d, ["m"])
    assert not has_path(d, ["m", "n"])
    assert has_path(d, ("i",))
    assert has_path(d, ("a", "b"))
    assert has_path(d, ["a", "f", "g"])

def test_has_path_list():
    assert has_path([1, 2], [0])
    assert not has_path([1, 2], [3])
    assert has_path({'x': [1, 2]}, ['x', 1])

def test_where():
    data = [{'a': 1, 'b': 2}, {'a': 10, 'b': 2}]
    assert isinstance(where(data, a=1), Iterator)
    assert list(where(data, a=1)) == [{'a': 1, 'b': 2}]

def test_lwhere():
    data = [{'a': 1, 'b': 2}, {'a': 10, 'b': 2}]
    assert lwhere(data, a=1, b=2) == [{'a': 1, 'b': 2}]
    assert lwhere(data, b=2) == data

    # Test non-existent key
    assert lwhere(data, c=1) == []

def test_pluck():
    data = [{'a': 1, 'b': 2}, {'a': 10, 'b': 2}]
    assert lpluck('a', data) == [1, 10]

def test_pluck_attr():
    TestObj = namedtuple('TestObj', ('id', 'name'))
    objs = [TestObj(1, 'test1'), TestObj(5, 'test2'), TestObj(10, 'test3')]
    assert lpluck_attr('id', objs) == [1, 5, 10]

def test_invoke():
    assert linvoke(['abc', 'def', 'b'], 'find', 'b') == [1, -1, 0]
