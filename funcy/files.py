
__all__ = ['slurp', 'spit']


def slurp(filename):
    """
    Read from file and return full content.
    """
    with open(filename, "r") as f:
        return f.read()


def spit(filename, content):
    """
    Write to file with given content.
    """
    with open(filename, "w") as f:
        f.write(content)
