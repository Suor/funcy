def partitioni(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    pool_limit = max(n * 2, 512)
    pool = take(n-1, it)
    for i, item in enumerate(it, start=n):
        pool.append(item)
        if len(pool) > pool_limit:
            pool = pool[-n:]
        if i % step == 0:
            yield pool[-n:]


from collections import deque
from itertools import islice


def partitionid(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    queue = deque(take(n-1, it), maxlen=n)

    for i, item in enumerate(it, start=n):
        queue.append(item)
        if i % step == 0:
            yield list(queue)

def partitionid2(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    queue = deque([], maxlen=n)
    for i, item in enumerate(seq, start=1):
        queue.append(item)
        if i % step == 0:
            yield list(queue)


def partitionid3(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    queue = deque(take(n, it), maxlen=n)
    while True:
        yield list(queue)
        new = take(step, it)
        if len(new) < step: break
        queue.extend(new)


def partitionis(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    pool_len = max(n, step)

    i = 0
    pool = []
    while True:
        # chunk = take(pool_len, it)
        # if not chunk: break
        # pool += chunk
        pool.extend(islice(it, pool_len))
        if len(pool) - i < n: break
        for i in range(i, len(pool)-n+1, step):
            # print 'ii', i
            yield pool[i:i+n]

        pool = pool[i:]
        i = step


def partitionis3(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    pool = take(n, it)
    while True:
        if len(pool) < n: break
        yield pool
        pool = pool[step:] + take(step, it)


def partitionis3a(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    pool = take(n, it)
    while True:
        if len(pool) < n: break
        yield pool
        pool = pool[step:]
        pool.extend(islice(it, step))


def partitionis2(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    it = iter(seq)
    while True:
        pool = take(n, it)
        if len(pool) == n:
            yield pool
        else:
            break
