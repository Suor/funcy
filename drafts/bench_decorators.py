# -*- coding: utf-8 -*-
import gc, time, sys
from functools import wraps

sys.path.insert(0, '/home/suor/projects/funcy')
from funcy import decorator


@decorator
def empty_funcy(call):
    return call()

def empty_old_school(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# import wrapt

# @wrapt.decorator
# def empty_wrapt(wrapped, instance, args, kwargs):
#     return wrapped(*args, **kwargs)

@decorator
def getx_funcy(call):
    return call.x

def getx_old_school(func):
    @wraps(func)
    def wrapper(x):
        return x
    return wrapper


def undecorated():
    return sum(range(20))

funcy_decorated = empty_funcy(undecorated)
funcy_decorated.__name__ = 'funcy_decorated'

old_school_decorated = empty_old_school(undecorated)
old_school_decorated.__name__ = 'old_school_decorated'

# wrapt_decorated = empty_wrapt(undecorated)
# wrapt_decorated.__name__ = 'wrapt_decorated'


def undecorated_getx(x):
    return x

funcy_getx = getx_funcy(undecorated_getx)
funcy_getx.__name__ = 'funcy_getx'

old_school_getx = getx_old_school(undecorated_getx)
old_school_getx.__name__ = 'funcy_getx'


def bench_test(test, *args):
    print 'Benchmarking %s ...' % test.__name__
    real, clock = 0, 0
    n = 1
    while real < 1:
        gc.disable()
        real, clock = bench_once(test, n, *args)
        gc.enable()
        n *= 2

    n /= 2
    # min_time = min(r[0] for r in l)
    # min_clock = min(r[1] for r in l)

    # return total * 2 / n # Or use normalized?
    # return min_clock
    print '%d loops, time %s, clock %s' % (n, format_time(real/n), format_time(clock/n))

def bench_once(test, n, *args):
    start = time.time()
    clock = time.clock()
    for _ in xrange(n):
        test(*args)
    return (time.time() - start, time.clock() - clock)

def format_time(sec):
    return '%07d ns' % (sec * 1e9)
    if sec < 1e-6:
        return '%s ns' % (sec * 1e9)
    elif sec < 1e-3:
        return '%s µs' % (sec * 1e6)
    elif sec < 1:
        return '%s ms' % (sec * 1e3)
    else:
        return '%s s' % sec

from profilehooks import profile


# bench_test(undecorated)
# bench_test(old_school_decorated)
# bench_test(funcy_decorated)
# # bench_test(wrapt_decorated)

# bench_test(undecorated_getx, 42)
# bench_test(old_school_getx, 42)
bench_test(funcy_getx, 42)
