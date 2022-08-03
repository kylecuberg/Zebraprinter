# Standard library
import time

# First-party/Local
import src.core
import src.util
from src import __version__


def test_version():
    assert __version__ == "0.2.1"


def test_core():
    # Pass
    assert src.core.main() is None


def test_util_seconds_but_readable():
    print("Now", src.util.seconds_but_readable(time.time()))


def test_util_loop_replace():
    test_str = src.util.loop_replace("A123", ["A", "1"])
    assert test_str == "23"
