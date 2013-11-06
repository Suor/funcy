from funcy.debug import *


def test_log_calls():
    log = []

    @log_calls(log.append)
    def f(x, y):
        return x + y


    f(1, 2)
    f('a', 'b')
    assert log == [
        "Call f(1, 2)",
        "-> 3 from f(1, 2)",
        "Call f('a', 'b')",
        "-> 'ab' from f('a', 'b')",
    ]
