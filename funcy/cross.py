try:
    from itertools import ifilter, imap, izip, ifilterfalse
    xrange = xrange  # noqa
    basestring = basestring  # noqa
    map = map
    filter = filter
except ImportError:
    ifilter, imap, izip = filter, map, zip
    from itertools import filterfalse as ifilterfalse  # noqa
    xrange = range
    basestring = (bytes, str)

    from builtins import map as _map, filter as _filter

    def map(f, *seqs):
        return list(_map(f, *seqs))

    def filter(f, seq):
        return list(_filter(f, seq))


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
