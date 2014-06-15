import sys, inspect
import pytest

import funcy
from funcy.cross import PY2, PY3
from funcy.py2 import cat

from funcy import py2, py3
py = py2 if PY2 else py3


# Introspect all modules
exclude = ('funcy.cross', 'funcy.py2', 'funcy.py3', 'funcy.simple_funcs', 'funcy.funcmakers')
modules = [m for m in funcy.__dict__.values()
             if inspect.ismodule(m)
                and m.__name__.startswith('funcy.') and m.__name__ not in exclude]


def test_match():
    assert funcy.__all__ == py.__all__


@pytest.mark.skipif(PY3, reason="modules use python 2 internally")
def test_full_py2():
    assert sorted(funcy.__all__) == sorted(cat(m.__all__ for m in modules))


def test_full():
    assert len(py2.__all__) == len(py3.__all__)
