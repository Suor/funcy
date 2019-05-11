try:
    # Python 3
    from itertools import filterfalse
    filter, map, zip, range = filter, map, zip, range  # noqa
    basestring = (bytes, str)

    def lmap(f, *seqs):
        return list(map(f, *seqs))

    def lfilter(f, seq):
        return list(filter(f, seq))

except ImportError:
    # Python 2
    lmap, lfilter, range = map, filter, xrange  # noqa
    from itertools import (ifilter as filter, imap as map, izip as zip,  # noqa
                          ifilterfalse as filterfalse)
    basestring = basestring  # noqa


# collections.abc was added in Python 3.3
try:
    from collections.abc import Mapping, Set, Sequence, Iterable, Iterator, Hashable  # noqa
except ImportError:
    from collections import Mapping, Set, Sequence, Iterable, Iterator, Hashable  # noqa


try:
    from contextlib import nullcontext
except ImportError:
    class nullcontext(object):
        """Context manager that does no additional processing.

        Used as a stand-in for a normal context manager, when a particular
        block of code is only sometimes used with a normal context manager:

        cm = optional_cm if condition else nullcontext()
        with cm:
            # Perform operation, using optional_cm if condition is True
        """

        def __init__(self, enter_result=None):
            self.enter_result = enter_result

        def __enter__(self):
            return self.enter_result

        def __exit__(self, *excinfo):
            pass


import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


# Taken from six and simplified
if PY3:
    exec("""def raise_from(value, from_value):
    try:
        raise value from from_value
    finally:
        value = None
""")
else:
    def raise_from(value, from_value):
        raise value
