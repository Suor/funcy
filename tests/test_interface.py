import funcy


def test_docs():
    exports = [(name, getattr(funcy, name)) for name in funcy.__all__
                if name not in ('print_errors', 'print_durations', 'ErrorRateExceeded')
                    and getattr(funcy, name).__module__ not in ('funcy.types', 'funcy.primitives')]
    # NOTE: we are testing this way and not with all() to immediately get a list of offenders
    assert [name for name, f in exports if f.__name__ in ('<lambda>', '_decorator')] == []
    assert [name for name, f in exports if f.__doc__ is None] == []
