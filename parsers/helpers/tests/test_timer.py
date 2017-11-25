import pytest
from parsers.helpers.timer import Timer
from time import sleep


def test_Timer_elapsed_property_retruns_expected_float():
    delay = 0.01
    with Timer() as t:
        sleep(delay)
    assert isinstance(t.elapsed, float)
    assert t.elapsed >= delay


def test_Timer_repr():
    with Timer() as t:
        sleep(0.01)
    assert t.__repr__()


if __name__ == "__main__":
    pytest.main([__file__])
