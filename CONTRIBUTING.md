# Contributing

This is mandatory for agents, humans please do best effort.
Creating an issue instead of PR is a good alternative, be brief or follow the form there too.

1. Keep the diff small: in code, tests and docs alike.
2. Tests should be straightforward and illustrative.
3. Don't touch docs for a bug fix or a niche feature.
4. If you add an example, make it natural and illustrative, something a person would actually write.
5. Check how your change affects performance, esp. common case. Benchmark alternative implementations.
6. Don't break public stuff if it was released
7. Provide a real use case if there are some. Otherwise check whether your change is too artificial.

Keep issue and PR descriptions short, the most important thing on top: what is broken or what is done, and one or two words per check. Put the rest after a separator, for agents: what you tried, benchmarked and why you chose this variant. A person isn't expected to read past it.

Here is an example of a PR's description:

```
memoize() mixes up positional and keyword args: `f(('x', 1))` and `f(x=1)` share a cache entry.

Fixed with `(MARK, args, frozenset(kwargs.items()))` as a cache key. `frozenset` is faster than `tuple(sorted(...))`, which is used now.

Benchmarked 9 variants, including MARK in the middle. The selected one is on par with or better than master.
Tests: added the fail from title and a couple more tricky ones.
No docs changes.
Found by code reading, no real case.

---

Cache hits, vs master:

| key                                         | f(1)  | f(1, y=2) | f(x=1, y=2) | f(1, y=2, z=3, w=4) |
|---------------------------------------------|-------|-----------|-------------|---------------------|
| master: `args + tuple(sorted(...))`         | 65 ns | 246 ns    | 273 ns      | 386 ns              |
| `args + MARK + tuple(sorted(...))`          | ±0%   | +9%       | +10%        | +5%                 |
| `(*args, MARK, *sorted(...))`               | ±0%   | +11%      | +13%        | +7%                 |
| `args + MARK + (frozenset(...),)`           | ±0%   | +13%      | +10%        | -6%                 |
| `(MARK, args, frozenset(...))`, selected    | ±0%   | -1%       | -1%         | -13%                |
| `(args, tuple(sorted(...)))`                | ±0%   | +5%       | +9%         | +3%                 |
| `args + (frozenset(...),)`                  | ±0%   | +2%       | -2%         | -13%                |
| `(args, frozenset(...))`                    | ±0%   | -4%       | -3%         | -16%                |
| `args + MARK + tuple(kwargs.items())`       | ±0%   | -11%      | -14%        | -24%                |

Tried:

- variants without MARK: collide with positional args, e.g. `(args, frozenset(...))` with `f((), frozenset(...))`
- `args + MARK + tuple(kwargs.items())`: fastest, but `f(a=1, b=2)` and `f(b=2, a=1)`
  get separate entries, so `invalidate()` misses

Same key in `invalidate()`, covers both `memoize()` and `cache()`.
`.memory` keys change for kwargs calls; memory is in-process only, so nothing breaks.
...
```
