from math import sin, cos
from funcy.calc import *


def test_make_lookuper():
    @make_lookuper
    def letter_index():
        return {c: i for i, c in enumerate('abcdefghij')}

    assert letter_index('c') == 2
    assert letter_index('_') is None


def test_make_lookuper_nested():
    tables_built = [0]

    @make_lookuper
    def function_table(f):
        tables_built[0] += 1
        return {x: f(x) for x in range(10)}

    assert function_table(sin)(5) == sin(5)
    assert function_table(cos)(3) == cos(3)
    assert function_table(sin)(3) == sin(3)
    assert tables_built[0] == 2
