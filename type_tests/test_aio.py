from collections.abc import AsyncIterator
from funcy import aio


async def numbers() -> AsyncIterator[int]:
    yield 1


async def stringify(x: int) -> str:
    return str(x)


async def positive(x: int) -> bool:
    return x > 0


async def expand(x: int) -> list[str]:
    return [str(x)]


async def add(x: int, y: int) -> int:
    return x + y


async def pipeline() -> None:
    reveal_type(aio.map(stringify, numbers()))  # R: AsyncIterator[str]
    reveal_type(aio.map(str, numbers()))  # R: AsyncIterator[str]
    reveal_type(aio.map(None, numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.lmap(stringify, numbers()))  # R: list[str]
    reveal_type(await aio.lmap({1: 'one'}, numbers()))  # R: list[str]
    reveal_type(aio.filter(positive, numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.lfilter(None, numbers()))  # R: list[int]
    reveal_type(aio.remove(positive, numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.lremove(positive, numbers()))  # R: list[int]
    reveal_type(aio.keep(numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.lkeep(stringify, numbers()))  # R: list[str]
    reveal_type(aio.drop(2, numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.take(2, aio.map(stringify, numbers())))  # R: list[str]
    reveal_type(await aio.first(numbers()))  # R: int | None
    reveal_type(await aio.second(numbers()))  # R: int | None
    reveal_type(await aio.nth(2, numbers()))  # R: int | None
    reveal_type(await aio.last(numbers()))  # R: int | None
    reveal_type(aio.rest(numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.ilen(numbers()))  # R: int
    reveal_type(aio.concat(numbers(), [1]))  # R: AsyncIterator[int]
    reveal_type(await aio.lconcat(numbers(), [1]))  # R: list[int]
    reveal_type(aio.cat([numbers()]))  # R: AsyncIterator[int]
    reveal_type(await aio.lcat([numbers()]))  # R: list[int]
    reveal_type(aio.mapcat(expand, numbers()))  # R: AsyncIterator[str]
    reveal_type(await aio.lmapcat(expand, numbers()))  # R: list[str]
    reveal_type(aio.takewhile(numbers()))  # R: AsyncIterator[int]
    reveal_type(aio.dropwhile(positive, numbers()))  # R: AsyncIterator[int]
    reveal_type(aio.distinct(numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.ldistinct(numbers(), stringify))  # R: list[int]
    reveal_type(await aio.group_by(stringify, numbers()))  # R: dict[str, list[int]]
    reveal_type(await aio.count_by(stringify, numbers()))  # R: dict[str, int]
    reveal_type(aio.chunks(2, numbers()))  # R: AsyncIterator[list[int]]
    reveal_type(await aio.lchunks(2, 1, numbers()))  # R: list[list[int]]
    reveal_type(aio.partition(2, 1, numbers()))  # R: AsyncIterator[list[int]]
    reveal_type(await aio.lpartition(2, numbers()))  # R: list[list[int]]
    reveal_type(aio.reductions(add, numbers()))  # R: AsyncIterator[int]
    reveal_type(await aio.lreductions(add, numbers(), 0))  # R: list[int]
    await aio.take('2', numbers())  # E: count must be an int
    aio.drop(2, 4)  # E: input must be iterable
    aio.filter(positive, 4)  # E: input must be iterable
