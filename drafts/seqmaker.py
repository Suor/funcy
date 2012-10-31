from itertools import groupby

inc = lambda x: x + 1
dec = lambda x: x - 1

def partition_by(f, coll):
    for _, group in groupby(coll, key=f):
        yield list(group)


def is_arithmetic(items):
    return len(items) == 2 \
        or len(items) >= 3 and items[-1] - items[-2] == items[-2] - items[-3]

def is_geometric(items):
    return len(items) >= 3 and items[-1] / items[-2] == items[-2] / items[-3]

def guess_succ(items, end):
    if is_geometric(items):
        koef = items[-1] / items[-2]
        return lambda x: x * koef
    elif is_arithmetic(items):
        step = items[-1] - items[-2]
        return lambda x: x + step
    else:
        return inc if end >= items[-1] else dec

def parse_key(key):
    is_ellipsis = lambda x: x is Ellipsis
    items, _, end = partition_by(is_ellipsis, key)
    assert len(items) >= 1
    assert len(end) == 1
    end = end[0]

    if callable(items[-1]) and len(items) > 1 and not callable(items[-2]):
        succ = items.pop()
    else:
        succ = guess_succ(items, end)

    assert len(items) >= 1
    return items, succ, end

def get_arity(succ, items):
    try:
        return int(succ.__code__.co_argcount)
    except (AttributeError, ValueError, TypeError):
        for n in range(len(items)):
            try:
                succ(*items[n:])
                return len(items) - n
            except TypeError:
                pass
        else:
            succ(*items) # reraise

class SeqMaker(object):
    def __getitem__(self, key):
        if isinstance(key, int):
            return range(1, key + 1)
        else:
            items, succ, end = parse_key(key)

            arity = get_arity(succ, items)
            while True:
                x = succ(*items[-arity:])
                if items[-1] < end < x or items[-1] > end > x:
                    break
                items.append(x)
                if x == end:
                    break

            return items

seq = SeqMaker()


from operator import __add__
from whatever import _

def test_seq():
    assert seq[1, ..., 3] == [1,2,3]
    assert seq[1, 3, ..., 9] == [1, 3, 5, 7, 9]
    assert seq[1, 2, 4, ..., 10] == [1, 2, 4, 8]
    assert seq[1, _ + 3, ..., 10] == [1, 4, 7, 10]
    assert seq[1, 1, _ + _, ..., 10] == [1, 1, 2, 3, 5, 8]
    assert seq[1, 1, __add__, ..., 10] == [1, 1, 2, 3, 5, 8]

    assert seq[3, ..., 1] == [3, 2, 1]
    assert seq[1, -2, 4, ..., 10] == [1, -2, 4, -8]
    assert seq[-1, 2, -4, ..., 10] == [-1, 2, -4, 8, -16]

    # seq[1, 10]
    # seq[10]
