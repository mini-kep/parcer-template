import pytest
from time import sleep
from parsers.timer import Timer

def test_Timer():
    t = Timer()
    delay = 0.25
    sleep(delay)
    t.stop()
    assert t.elapsed >= 0.25

if __name__ == '__main__':
    pytest.main([__file__])
    