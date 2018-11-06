import os

import funcy

def test_slurp_and_spit():
    filename = "test_slurp_and_spit.txt"
    content = "The quick brown fox jumps over the lazy dog"

    # Blank slate
    if os.path.exists(filename):
        os.remove(filename)

    # Spit
    funcy.spit(filename, content)
    assert os.path.exists(filename)

    # Slurp
    text_from_file = funcy.slurp(filename)
    assert content == text_from_file

    # Clean up
    os.remove(filename)
