from typing import assert_type
from funcy import cached_property, cached_readonly, monkey, LazyObject

# -- cached_property --
class MyClass:
    @cached_property
    def value(self) -> int:
        return 42

    @cached_readonly
    def ro_value(self) -> str:
        return "hello"

obj = MyClass()
assert_type(obj.value, int)
assert_type(obj.ro_value, str)

# -- LazyObject --
lazy = LazyObject(lambda: [1, 2, 3])
assert_type(lazy, LazyObject)

# -- monkey --
class Target:
    pass

@monkey(Target)
def new_method(self: Target) -> int:
    return 42

# -- Should be errors --
cached_property(42)  # E: not a callable
