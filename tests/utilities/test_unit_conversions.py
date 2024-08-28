""" Unit tests for the unit_conversions module. """

import pytest

from pyosirix_example.utilities.unit_conversions import convert_kg_to_lb


def test_convert_kg_to_lb():
    assert convert_kg_to_lb(1) == pytest.approx(2.20462, abs=1e-6), \
        f"bad conversion for 1"
    assert convert_kg_to_lb(0) == pytest.approx(0, abs=1e-6), \
        f"bad conversion for 0"
    assert convert_kg_to_lb(100) == pytest.approx(220.462, abs=1e-6), \
        f"bad conversion for 100"
    assert convert_kg_to_lb(2.5) == pytest.approx(5.51155, abs=1e-6), \
        f"bad conversion for 2.5"
    assert convert_kg_to_lb(0.001) == pytest.approx(0.00220462, abs=1e-6), \
        f"bad conversion for 0.001"


def test_convert_kg_to_lb_negative_value():
    # Test that a negative weight raises a ValueError with the correct message returned.
    with pytest.raises(ValueError, match="weight_kg must be positive!"):
        convert_kg_to_lb(-1)
