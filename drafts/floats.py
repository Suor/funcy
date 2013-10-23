"""
A couple of floating point utilities.

Not sure they should go into funcy.
"""

import math


def fround(value, base):
    return math.floor(value / base) * base

def frange(start, end, step):
    int_start = int(round(start / step))
    int_end = int(round(end / step))
    for i in xrange(int_start, int_end):
        yield i * step


from itertools import count

def frange2(start, end, step):
    for i in count():
        value = start + i * step
        if value > end: break
        yield value
