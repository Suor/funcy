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

def partitionis(n, step, seq=EMPTY):
    if seq is EMPTY:
        step, seq = n, step

    i = 0
    it = iter(seq)
    while True:
        tmp, it = tee(it)
        l = list(islice(tmp, i, i+n))
        if len(l) == n:
            yield l
        else:
            break

    # queue = deque([], maxlen=n)
    # for i, item in enumerate(seq, start=1):
    #     queue.append(item)
    #     if i % step == 0:
    #         yield list(queue)
