import sys


# Keep the synchronous package/test suite usable on pre-async-generator Python.
collect_ignore = ['test_aio.py'] if sys.version_info < (3, 6) else []
