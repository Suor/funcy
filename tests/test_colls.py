from funcy.colls import *
from whatever import _


def test_walk_values():
    assert walk_values(_ * 2, {'a': 1, 'b': 2}) == {'a': 2, 'b': 4}

def test_select_values():
    assert select_values(_ % 2, {'a': 1, 'b': 2}) == {'a': 1}

def test_all():
    assert all([1,2,3])
    assert not all([1,2,''])
    assert all(callable, [abs, open, int])
    assert not all(_ < 3, [1,2,5])

def test_any():
    assert any([0, False, 3, ''])
    assert any([0, False, '']) == False
    assert any(_ > 0, [1,2,0])
    assert any(_ < 0, [1,2,0]) == False

def test_none():
    assert none([0, False])
    assert none(_ < 0, [0, -1]) == False

def test_some():
    assert some([0, '', 2, 3]) == 2
    assert some(_ > 3, range(10)) == 4
