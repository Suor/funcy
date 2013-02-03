# from collections import Iterator
# import pytest
# from whatever import _

from funcy.decorators import *


def test_decorator_no_args():
    @decorator
    def inc(call):
        return call() + 1

    @inc
    def ten():
        return 10

    assert ten() == 11


def test_decorator_with_args():
    @decorator
    def add(call, n):
        return call() + n

    @add(2)
    def ten():
        return 10

    assert ten() == 12
