from typing import assert_type
from funcy import isnone, notnone, inc, dec, even, odd

# -- isnone / notnone --
assert_type(isnone(None), bool)
assert_type(isnone(42), bool)
assert_type(notnone(None), bool)
assert_type(notnone("hello"), bool)

# -- inc / dec --
n: int = 1
assert_type(inc(n), int)
assert_type(dec(n), int)

# -- even / odd --
assert_type(even(4), bool)
assert_type(odd(3), bool)

# -- Should be errors --
inc("x")  # E: wrong argument type
dec("x")  # E: wrong argument type
even("x")  # E: wrong argument type
odd("x")  # E: wrong argument type
