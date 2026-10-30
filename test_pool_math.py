import pytest

from pool_math import chlorine_status


def test_low_reading():
    assert chlorine_status(0.5) == "low"


def test_ok_reading():
    assert chlorine_status(2.0) == "ok"


def test_high_reading():
    assert chlorine_status(4.5) == "high"


@pytest.mark.parametrize("ppm", [1.0, 3.0])
def test_edges_are_ok(ppm):
    assert chlorine_status(ppm) == "ok"


def test_negative_reading_rejected():
    with pytest.raises(ValueError):
        chlorine_status(-1)
