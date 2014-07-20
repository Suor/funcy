import re, time

from funcy.debug import *
from funcy.flow import silent


def test_tap():
    assert capture(tap, 42) == '42\n'
    assert capture(tap, 42, label='Life and ...') == 'Life and ...: 42\n'


def test_log_calls():
    log = []

    @log_calls(log.append)
    def f(x, y):
        return x + y

    f(1, 2)
    f('a', 'b')
    assert log == [
        "Call f(1, 2)",
        "-> 3 from f(1, 2)",
        "Call f('a', 'b')",
        "-> 'ab' from f('a', 'b')",
    ]


def test_log_calls_raise():
    log = []

    @log_calls(log.append, stack=False)
    def f():
        raise Exception('something bad')

    silent(f)()
    assert log == [
        "Call f()",
        "-> Exception: something bad raised in f()",
    ]


def test_log_errors():
    log = []

    @log_errors(log.append)
    def f(x):
        return 1 / x

    silent(f)(1)
    silent(f)(0)
    assert len(log) == 1
    assert log[0].startswith('Traceback')
    assert re.search(r'ZeroDivisionError: .*\n    raised in f\(0\)$', log[0])


def test_log_durations():
    log = []

    @log_durations(log.append)
    def f():
        time.sleep(0.010)

    f()
    m = re.search(r'^\s*(\d+\.\d+) ms in f\(\)$', log[0])
    assert m
    assert 10 <= float(m.group(1)) < 20


### An utility to capture stdout

import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

def capture(command, *args, **kwargs):
    out, sys.stdout = sys.stdout, StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        return sys.stdout.read()
    finally:
        sys.stdout = out
