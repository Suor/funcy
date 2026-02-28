"""Tests for the .pyih -> .pyi translator."""
import pytest
from translate_pyih import parse_pyih, generate_func_group, generate_pyi


def get_func_output(source):
    """Parse source and return generated output for all func groups."""
    items = parse_pyih(source)
    results = []
    for item in items:
        if item['kind'] == 'func_group':
            results.append(generate_func_group(item))
    return results


def get_single_func(source):
    """Parse source and return generated output for a single func group."""
    results = get_func_output(source)
    assert len(results) == 1, f"Expected 1 func group, got {len(results)}"
    return results[0]


class TestPassthrough:
    """Functions without XFunc/XPred/C pass through unchanged."""

    def test_simple_function(self):
        out = get_single_func(
            "def take(n: int, seq: Iterable[_T]) -> list[_T]: ..."
        )
        assert out == "def take(n: int, seq: Iterable[_T]) -> list[_T]: ..."

    def test_no_params(self):
        out = get_single_func("def merge() -> None: ...")
        assert out == "def merge() -> None: ..."

    def test_multiple_overloads_get_decorator(self):
        source = (
            "def partition(n: int, seq: Iterable[_T]) -> Iterator[list[_T]]: ...\n"
            "def partition(n: int, step: int, seq: Iterable[_T]) -> Iterator[list[_T]]: ..."
        )
        out = get_single_func(source)
        assert out.count("@overload") == 2
        assert out.count("def partition(") == 2

    def test_single_function_no_overload_decorator(self):
        out = get_single_func("def first(seq: Iterable[_T]) -> _T | None: ...")
        assert "@overload" not in out


class TestXFunc:
    """XFunc[[A], B] expands to 7 overload variants."""

    def test_basic_expansion(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        assert out.count("@overload") == 7
        assert out.count("def map(") == 7

    def test_callable_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        assert "def map(f: Callable[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..." in out

    def test_none_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        # None: B becomes A (identity)
        assert "def map(f: None, seq: Iterable[_T]) -> Iterator[_T]: ..." in out

    def test_set_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        # Set: B becomes bool
        assert "def map(f: AbstractSet[_T], seq: Iterable[_T]) -> Iterator[bool]: ..." in out

    def test_regex_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        # Regex: A becomes Any, B becomes _ReResult | None
        assert ("def map(f: str | bytes | re.Pattern[str], seq: Iterable[Any]) "
                "-> Iterator[_ReResult | None]: ...") in out

    def test_int_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        # int: A becomes Sequence[_T], B becomes _T
        assert "def map(f: int, seq: Iterable[Sequence[_T]]) -> Iterator[_T]: ..." in out

    def test_slice_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        # slice: A becomes Sequence[_T], B becomes Sequence[_T]
        assert ("def map(f: slice, seq: Iterable[Sequence[_T]]) "
                "-> Iterator[Sequence[_T]]: ...") in out

    def test_mapping_variant(self):
        out = get_single_func(
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ..."
        )
        # Mapping: A->key, B->value
        assert "def map(f: Mapping[_T, _V], seq: Iterable[_T]) -> Iterator[_V]: ..." in out

    def test_skip_variant(self):
        source = (
            "# xfunc_skip: slice\n"
            "def walk_keys(f: XFunc[[_K], _K2], coll: Mapping[_K, _V]) -> dict[_K2, _V]: ..."
        )
        out = get_single_func(source)
        assert out.count("def walk_keys(") == 6  # 7 - 1 skipped
        assert "f: slice" not in out

    def test_extra_overload_alongside_xfunc(self):
        source = (
            "def map(f: XFunc[[_T], _V], seq: Iterable[_T]) -> Iterator[_V]: ...\n"
            "def map(f: Callable[..., _V], *seqs: Iterable[Any]) -> Iterator[_V]: ..."
        )
        out = get_single_func(source)
        # 7 XFunc variants + 1 passthrough = 8
        assert out.count("def map(") == 8
        assert "def map(f: Callable[..., _V], *seqs: Iterable[Any]) -> Iterator[_V]: ..." in out

    def test_typevar_no_partial_match(self):
        """_K should not match _K2 during substitution."""
        out = get_single_func(
            "def walk_keys(f: XFunc[[_K], _K2], coll: dict[_K, _V]) -> dict[_K2, _V]: ..."
        )
        # int variant: _K -> Sequence[_T], _K2 -> _T
        assert "def walk_keys(f: int, coll: dict[Sequence[_T], _V]) -> dict[_T, _V]: ..." in out
        # Should NOT have mangled _K2 into Sequence[_T]2
        assert "Sequence[_T]2" not in out


class TestXPred:
    """XPred[A] expands to 7 overload variants preserving element type."""

    def test_basic_expansion(self):
        out = get_single_func(
            "def filter(pred: XPred[_T], seq: Iterable[_T]) -> Iterator[_T]: ..."
        )
        assert out.count("@overload") == 7
        assert out.count("def filter(") == 7

    def test_callable_variant(self):
        out = get_single_func(
            "def filter(pred: XPred[_T], seq: Iterable[_T]) -> Iterator[_T]: ..."
        )
        assert "def filter(pred: Callable[[_T], Any], seq: Iterable[_T]) -> Iterator[_T]: ..." in out

    def test_none_variant(self):
        out = get_single_func(
            "def filter(pred: XPred[_T], seq: Iterable[_T]) -> Iterator[_T]: ..."
        )
        assert "def filter(pred: None, seq: Iterable[_T]) -> Iterator[_T]: ..." in out

    def test_regex_constrains_to_str(self):
        out = get_single_func(
            "def filter(pred: XPred[_T], seq: Iterable[_T]) -> Iterator[_T]: ..."
        )
        # Regex pred constrains elements to str
        assert ("def filter(pred: str | bytes | re.Pattern[str], "
                "seq: Iterable[str]) -> Iterator[str]: ...") in out

    def test_mapping_preserves_element(self):
        out = get_single_func(
            "def filter(pred: XPred[_T], seq: Iterable[_T]) -> Iterator[_T]: ..."
        )
        assert ("def filter(pred: Mapping[_T, Any], "
                "seq: Iterable[_T]) -> Iterator[_T]: ...") in out

    def test_set_preserves_element(self):
        out = get_single_func(
            "def filter(pred: XPred[_T], seq: Iterable[_T]) -> Iterator[_T]: ..."
        )
        assert ("def filter(pred: AbstractSet[_T], "
                "seq: Iterable[_T]) -> Iterator[_T]: ...") in out

    def test_return_type_preserved(self):
        """XPred preserves element type in complex return types."""
        out = get_single_func(
            "def split(pred: XPred[_T], seq: Iterable[_T]) -> "
            "tuple[Iterator[_T], Iterator[_T]]: ..."
        )
        # Callable variant
        assert "-> tuple[Iterator[_T], Iterator[_T]]: ..." in out
        # Regex variant constrains _T to str
        assert "-> tuple[Iterator[str], Iterator[str]]: ..." in out


class TestCollectionExpansion:
    """[C: (type1, type2)] expands to per-type overloads."""

    def test_basic_expansion(self):
        out = get_single_func(
            "def walk[C: (list, set)](f: Callable[[_T], _V], coll: C[_T]) -> C[_V]: ..."
        )
        assert out.count("def walk(") == 2
        assert "coll: list[_T]) -> list[_V]: ..." in out
        assert "coll: set[_T]) -> set[_V]: ..." in out

    def test_two_param_types(self):
        out = get_single_func(
            "def walk_keys[C: (dict, Mapping)](f: Callable[[_K], _K2], "
            "coll: C[_K, _V]) -> C[_K2, _V]: ..."
        )
        assert "coll: dict[_K, _V]) -> dict[_K2, _V]: ..." in out
        assert "coll: Mapping[_K, _V]) -> Mapping[_K2, _V]: ..." in out


class TestCollectionWithXFunc:
    """[C: (...)] × XFunc gives quadratic expansion."""

    def test_quadratic_count(self):
        out = get_single_func(
            "def walk[C: (list, set)](f: XFunc[[_T], _V], coll: C[_T]) -> C[_V]: ..."
        )
        # 7 XFunc variants × 2 collection types = 14
        assert out.count("def walk(") == 14

    def test_collection_type_preserved(self):
        out = get_single_func(
            "def walk[C: (list, set)](f: XFunc[[_T], _V], coll: C[_T]) -> C[_V]: ..."
        )
        # list: Callable variant
        assert "def walk(f: Callable[[_T], _V], coll: list[_T]) -> list[_V]: ..." in out
        # set: Callable variant
        assert "def walk(f: Callable[[_T], _V], coll: set[_T]) -> set[_V]: ..." in out
        # list: None variant
        assert "def walk(f: None, coll: list[_T]) -> list[_T]: ..." in out
        # set: int variant
        assert "def walk(f: int, coll: set[Sequence[_T]]) -> set[_T]: ..." in out


class TestCollectionWithXPred:
    """[C: (...)] × XPred gives quadratic expansion with type preservation."""

    def test_quadratic_count(self):
        out = get_single_func(
            "def select_keys[C: (dict, Mapping)](pred: XPred[_K], "
            "coll: C[_K, _V]) -> C[_K, _V]: ..."
        )
        # 7 XPred variants × 2 collection types = 14
        assert out.count("def select_keys(") == 14

    def test_dict_preserved(self):
        out = get_single_func(
            "def select_keys[C: (dict, Mapping)](pred: XPred[_K], "
            "coll: C[_K, _V]) -> C[_K, _V]: ..."
        )
        assert ("def select_keys(pred: Callable[[_K], Any], "
                "coll: dict[_K, _V]) -> dict[_K, _V]: ...") in out

    def test_mapping_preserved(self):
        out = get_single_func(
            "def select_keys[C: (dict, Mapping)](pred: XPred[_K], "
            "coll: C[_K, _V]) -> C[_K, _V]: ..."
        )
        assert ("def select_keys(pred: Callable[[_K], Any], "
                "coll: Mapping[_K, _V]) -> Mapping[_K, _V]: ...") in out

    def test_regex_constrains_key_in_both(self):
        out = get_single_func(
            "def select_keys[C: (dict, Mapping)](pred: XPred[_K], "
            "coll: C[_K, _V]) -> C[_K, _V]: ..."
        )
        assert ("def select_keys(pred: str | bytes | re.Pattern[str], "
                "coll: dict[str, _V]) -> dict[str, _V]: ...") in out
        assert ("def select_keys(pred: str | bytes | re.Pattern[str], "
                "coll: Mapping[str, _V]) -> Mapping[str, _V]: ...") in out


class TestVerbatimPreservation:
    """Non-function content is preserved."""

    def test_imports_preserved(self):
        source = "import re\nfrom typing import Any\n"
        out = generate_pyi(source, "test.pyih")
        assert "import re" in out
        assert "from typing import Any" in out

    def test_comments_preserved(self):
        source = "# A comment\ndef take(n: int) -> int: ...\n"
        out = generate_pyi(source, "test.pyih")
        assert "# A comment" in out

    def test_comments_between_different_functions(self):
        source = (
            "def foo(x: int) -> int: ...\n"
            "\n"
            "# Section header\n"
            "\n"
            "def bar(x: int) -> int: ...\n"
        )
        out = generate_pyi(source, "test.pyih")
        assert "# Section header" in out
        assert "def foo(" in out
        assert "def bar(" in out

    def test_comments_between_same_function_overloads(self):
        source = (
            "def walk[C: (list, set)](f: XFunc[[_T], _V], coll: C[_T]) -> C[_V]: ...\n"
            "# dict overload\n"
            "def walk(f: Callable[[_K], _V], coll: dict[_K, _V]) -> dict[_K, _V]: ...\n"
        )
        out = get_single_func(source)
        # All walk overloads should be in one group
        assert out.count("def walk(") == 15  # 7×2 + 1 passthrough


class TestGeneratedHeader:
    """Generated files get a header."""

    def test_header(self):
        out = generate_pyi("def f(x: int) -> int: ...\n", "test.pyih")
        assert "AUTOGENERATED by translate_pyih.py from test.pyih" in out
        assert "DO NOT EDIT" in out
