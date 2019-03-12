import pkgutil
import pytest

from funcy.compat import PY2, PY3
import funcy
from funcy import py2, py3
from funcy.py3 import cat, lcat, count_reps, is_iter, is_list


# Introspect all modules
exclude = ('compat', 'cross', '_inspect', 'py2', 'py3', 'simple_funcs', 'funcmakers')
module_names = list(name for _, name, _ in pkgutil.iter_modules(funcy.__path__)
                    if name not in exclude)
modules = [getattr(funcy, name) for name in module_names]


def test_match():
    assert funcy.__all__ == (py2 if PY2 else py3).__all__


@pytest.mark.skipif(PY2, reason="modules use python 3 internally")
def test_full_py3():
    assert sorted(funcy.__all__) == sorted(lcat(m.__all__ for m in modules) + ['lzip'])


def test_full():
    assert len(py2.__all__) == len(py3.__all__)


def test_name_clashes():
    counts = count_reps(cat(m.__all__ for m in modules))
    clashes = [name for name, c in counts.items() if c > 1]
    assert not clashes, 'names clash for ' + ', '.join(clashes)


def test_renames():
    inames = [n for n in py2.__all__ if n.startswith('i')]
    ipairs = [n[1:] for n in inames if n[1:] in py2.__all__]

    for name in inames:
        if name != 'izip':
            assert name in py3.__all__ or name[1:] in py3.__all__

    for name in ipairs:
        assert name in py3.__all__
        assert 'l' + name in py3.__all__

    lnames = [n for n in py3.__all__ if n.startswith('l')]
    lpairs = [n[1:] for n in lnames if n[1:] in py3.__all__]

    for name in lnames:
        if name != 'lzip':
            assert name in py2.__all__ or name[1:] in py2.__all__

    for name in lpairs:
        assert name in py2.__all__
        assert 'i' + name in py2.__all__

    # Only inames a renamed
    assert set(py2.__all__) - set(py3.__all__) <= set(inames)
    # Only lnames a new, and zip_values/zip_dicts
    assert set(py3.__all__) - set(py2.__all__) <= set(lnames) | set(['zip_values', 'zip_dicts'])


def test_docs():
    exports = [(name, getattr(funcy, name)) for name in funcy.__all__
                if name not in ('print_errors', 'print_durations', 'ErrorRateExceeded')
                    and getattr(funcy, name).__module__ not in ('funcy.types', 'funcy.primitives')]
    # NOTE: we are testing this way and not with all() to immediately get a list of offenders
    assert [name for name, f in exports if f.__name__ in ('<lambda>', '_decorator')] == []
    assert [name for name, f in exports if f.__doc__ is None] == []


def test_list_iter():
    assert is_list(py2.map(None, []))
    assert is_iter(py3.map(None, []))
    assert is_list(funcy.map(None, [])) == PY2
    assert is_iter(funcy.map(None, [])) == PY3
