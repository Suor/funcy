from contextlib import contextmanager

import pytest

from funcy import wrap_with


@pytest.mark.parametrize('suppress_error', [False, True])
def test_wrap_with_generator_context_after_error(suppress_error):
    events = []
    error = ValueError('cannot save')

    @contextmanager
    def transaction():
        events.append('begin')
        try:
            yield
        except ValueError:
            events.append('error')
            if not suppress_error:
                raise
        finally:
            events.append('end')

    @wrap_with(transaction())
    def save(fail):
        events.append('save')
        if fail:
            raise error
        return 'saved'

    if suppress_error:
        assert save(True) is None
    else:
        with pytest.raises(ValueError) as caught:
            save(True)
        assert caught.value is error

    assert save(False) == 'saved'
    assert events == ['begin', 'save', 'error', 'end', 'begin', 'save', 'end']
