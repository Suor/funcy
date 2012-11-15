from whatever import _

from funcy.funcolls import *


def test_all_fn():
    assert filter(all_fn(_ > 3, _ % 2), range(10)) == [5, 7, 9]

def test_any_fn():
    assert filter(any_fn(_ > 3, _ % 2), range(10)) == [1, 3, 4, 5, 6, 7, 8, 9]

def test_none_fn():
    assert filter(none_fn(_ > 3, _ % 2), range(10)) == [0, 2]

def test_some_fn():
    assert some_fn(_-1, _*0, _+1, _*2)(1) == 2
