import pytest

from testtest.tester import inc

def test_inc():
    assert inc(4) == 5
    assert inc(0) == 1
    assert inc(-1) == 0
