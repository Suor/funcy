from funcy.flow import *


def test_silent():
    assert silent(int)(1) == 1
    assert silent(int)('1') == 1
    assert silent(int)('hello') is None
