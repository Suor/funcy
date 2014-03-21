# -*- coding: utf-8 -*-
import gc, time, sys
sys.path.insert(0, '/home/suor/projects/funcy')
from funcy import *
# import funcy

@decorator
def empty_f(call):
    return call()

from functools import wraps

def empty_f2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

import wrapt

@wrapt.decorator
def empty_wrapt(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)


f = lambda x: x
f1 = empty_f(f)
f2 = empty_f2(f)
fw = empty_wrapt(f)

l = range(100)

def undecorated():
    return map(f, l)
def old_school_decorated():
    return map(f2, l)
def funcy_decorated():
    return map(f1, l)
def wrapt_decorated():
    return map(fw, l)

def bench_test(test):
    print 'Benchmarking %s ...' % test.__name__
    real, clock = 0, 0
    n = 1
    while real < 1:
        gc.disable()
        real, clock = bench_once(test, n)
        gc.enable()
        n *= 2

    n /= 2
    # min_time = min(r[0] for r in l)
    # min_clock = min(r[1] for r in l)

    # return total * 2 / n # Or use normalized?
    # return min_clock
    print '%d loops, time %s, clock %s' % (n, format_time(real/n), format_time(clock/n))

def bench_once(test, n):
    start = time.time()
    clock = time.clock()
    for _ in xrange(n):
        test()
    return (time.time() - start, time.clock() - clock)

def format_time(sec):
    if sec < 1e-6:
        return '%s ns' % (sec * 1e9)
    elif sec < 1e-3:
        return '%s µs' % (sec * 1e6)
    elif sec < 1:
        return '%s ms' % (sec * 1e3)
    else:
        return '%s s' % sec


bench_test(undecorated)
bench_test(old_school_decorated)
bench_test(funcy_decorated)
bench_test(wrapt_decorated)
