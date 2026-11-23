import asyncio
import functools
import operator

import pytest

import funcy
from funcy import aio
from funcy.primitives import EMPTY


def run_async(f):
    @functools.wraps(f)
    def run(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(f(*args, **kwargs))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
    return run


async def stream(items):
    for item in items:
        yield item


async def double(x):
    await asyncio.sleep(0)
    return x * 2


async def odd(x):
    await asyncio.sleep(0)
    return x % 2


@run_async
async def test_pipeline_and_partial_consumption():
    source = stream(range(20))
    pipeline = aio.map(double, aio.drop(2, aio.filter(odd, source)))
    assert await aio.take(3, pipeline) == [10, 14, 18]
    assert await source.__anext__() == 10
    assert await aio.take(0, pipeline) == []
    assert await aio.first(pipeline) == 22


@pytest.mark.parametrize('f', [operator.neg, double, None, {1: 3, 2: 4}])
@run_async
async def test_mappers(f):
    expected = [2, 4] if f is double else funcy.lmap(f, [1, 2])
    assert await aio.lmap(f, stream([1, 2])) == expected


@run_async
async def test_extended_functions_and_mixed_inputs():
    assert await aio.lmap('x(.)', ['xa', 'xb', 'n']) == ['a', 'b', None]
    assert await aio.lmap(1, stream([(1, 2), (3, 4)])) == [2, 4]
    assert await aio.lfilter({1, 3}, stream(range(5))) == [1, 3]
    assert await aio.lfilter('^a', ['a', 'bad', 'abc']) == ['a', 'abc']
    assert await aio.lmap(operator.add, stream([1, 2]), [10, 20, 30]) == [11, 22]
    with pytest.raises(TypeError):
        aio.map(None)


@pytest.mark.parametrize('factory', [list, stream])
@run_async
async def test_selection(factory):
    assert await aio.take(8, factory(range(3))) == [0, 1, 2]
    assert await aio.lmap(None, aio.drop(8, factory(range(3)))) == []
    assert await aio.first(factory([])) is None
    assert await aio.second(factory(range(3))) == 1
    assert await aio.nth(2, factory(range(3))) == 2
    assert await aio.nth(3, factory(range(3))) is None
    assert await aio.last(factory(range(3))) == 2
    assert await aio.last(factory([])) is None
    assert await aio.ilen(aio.rest(factory(range(3)))) == 2
    assert await aio.nth(-1, [1, 2]) == 2
    for n in [-1, -3]:
        with pytest.raises(ValueError):
            await aio.take(n, factory(range(3)))
        with pytest.raises(ValueError):
            aio.drop(n, factory(range(3)))
    with pytest.raises(TypeError):
        await aio.take(1.5, factory(range(3)))


@run_async
async def test_predicates_keep_and_while():
    assert await aio.lfilter(odd, stream(range(6))) == [1, 3, 5]
    assert await aio.lremove(odd, stream(range(6))) == [0, 2, 4]
    assert await aio.lkeep(stream([0, 1, None, 2])) == [1, 2]
    assert await aio.lkeep(double, stream(range(3))) == [2, 4]
    assert await aio.lmap(None, aio.takewhile(stream([1, 2, 0, 3]))) == [1, 2]
    assert await aio.lmap(None, aio.dropwhile(stream([1, 2, 0, 3]))) == [0, 3]
    source = stream([1, 3, 2, 5])
    assert await aio.lmap(None, aio.takewhile(odd, source)) == [1, 3]
    assert await source.__anext__() == 5
    assert await aio.lmap(None, aio.dropwhile(odd, stream([1, 3, 2, 5]))) == [2, 5]


@run_async
async def test_concatenation():
    assert await aio.lconcat([1, 2], stream([3]), []) == [1, 2, 3]
    assert await aio.lcat(stream([[1], stream([2, 3])])) == [1, 2, 3]
    assert await aio.lmapcat(lambda x: stream([x, x]), [1, 2]) == [1, 1, 2, 2]
    assert await aio.lmapcat(lambda a, b: [a, b], [1, 2], stream([3])) == [1, 3]
    assert await aio.lcat([]) == []


@run_async
async def test_distinct_and_grouping():
    assert await aio.ldistinct(stream([1, 2, 1])) == [1, 2]
    assert await aio.ldistinct(stream(range(5)), odd) == [0, 1]
    assert await aio.ldistinct([{'id': 1}, {'id': 1}], lambda x: x['id']) == [{'id': 1}]
    assert await aio.group_by(odd, stream(range(5))) == {0: [0, 2, 4], 1: [1, 3]}
    assert await aio.count_by(odd, stream(range(5))) == {0: 3, 1: 2}
    assert await aio.group_by(None, []) == {}


@pytest.mark.parametrize('name', ['chunks', 'partition'])
@pytest.mark.parametrize('n,step', [(3, 1), (3, 3), (3, 5), (1, 1), (8, 2)])
@run_async
async def test_chunking_matches_synchronous(name, n, step):
    eager = getattr(aio, 'l' + name)
    sync = getattr(funcy, 'l' + name)
    assert await eager(n, step, stream(range(7))) == sync(n, step, iter(range(7)))
    assert await eager(n, stream(range(7))) == sync(n, iter(range(7)))
    assert await eager(n, step, []) == []
    with pytest.raises(ValueError):
        getattr(aio, name)(0, [1])
    with pytest.raises(ValueError):
        getattr(aio, name)(n, -1, [1])


@run_async
async def test_reductions():
    async def add(a, b):
        return a + b
    assert await aio.lreductions(add, stream(range(4))) == [0, 1, 3, 6]
    assert await aio.lreductions(add, stream(range(4)), 10) == [10, 11, 13, 16]
    assert await aio.lreductions(add, [], 10) == []
    assert await aio.lreductions(lambda a, b: b, [EMPTY, 1]) == [EMPTY, 1]


@run_async
async def test_awaitable_return_values_and_callback_failures():
    def future(x):
        result = asyncio.get_event_loop().create_future()
        result.set_result(x + 1)
        return result
    assert await aio.lmap(future, [1, 2]) == [2, 3]
    def fail(x):
        raise ValueError('callback failed')
    with pytest.raises(ValueError, match='callback failed'):
        await aio.lmap(fail, [1])
    async def failed_source():
        yield 1
        raise OSError('stream failed')
    with pytest.raises(OSError, match='stream failed'):
        await aio.lmap(None, failed_source())
    def stop(x):
        raise StopAsyncIteration('callback, not input exhaustion')
    with pytest.raises(RuntimeError, match='StopAsyncIteration'):
        await aio.lmap(stop, [1])


@run_async
async def test_cancellation_and_borrowed_input():
    started = asyncio.Event()
    gate = asyncio.Event()
    async def blocked(x):
        started.set()
        await gate.wait()
        return x
    source = stream(range(4))
    task = asyncio.ensure_future(aio.lmap(blocked, source))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert await source.__anext__() == 1
    mapped = aio.map(None, source)
    assert await mapped.__anext__() == 2
    await mapped.aclose()
    assert await source.__anext__() == 3


def test_import_does_not_replace_synchronous_helpers():
    assert funcy.lmap(operator.neg, [1, 2]) == [-1, -2]
    assert funcy.take(1, [1, 2]) == [1]
    assert 'aio' not in funcy.__all__
