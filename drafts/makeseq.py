# (start)
# (start, step)
# (*start, succ)
# (start, end)
# (start, step, end)
# (*start, succ, end)
# (start, stop)
# (start, step, stop)
# (*start, succ, stop)


from collections import deque

def iseq(*args):
    start, succ, stop = args[:-2], args[-2], args[-1]

    for x in start:
        if stop(x): break
        yield x

    items = deque(start)
    while True:
        x = succ(*items)
        if stop(x): break
        yield x
        items.popleft()
        items.append(x)


from whatever import _

def test_iseq():
    assert list(iseq(1, _+1, _>10)) == [1,2,3,4,5,6,7,8,9,10]
    assert list(iseq(1, _*2, _>10)) == [1,2,4,8]

# def overload(*args):
#     pass

# @overload(Ellipsis, callable, callable)
# def iseq(start, succ, stop):
#     pass
