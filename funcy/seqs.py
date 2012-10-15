from itertools import repeat, islice

# NOTE: Should I import here anything from itertools or elsewhere,
#       if it exactly implements some function I want?
# PROS: Convenient
# CONS: Possibly confusing

# pythons itertools.repeat() is basically the same as in clojure

def repeatedly(f, n=None):
    _repeat = repeat(None, n) if n else repeat(None)
    return (f() for _ in _repeat)

def iterate(f, x):
    while True:
        yield x
        x = f(x)

def take(n, coll):
    return list(islice(coll, n))

# TODO: tree-seq equivalent


from itertools import count


def test_repeatedly():
    c = count().next
    assert take(2, repeatedly(c)) == [0, 1]
