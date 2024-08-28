""" An example test file to demonstrate local fixture sharing. """

import pytest
import numpy as np


@pytest.fixture(scope="function")
def local_data():
    """ This fixture can only be used in this module. """
    yield [-2, -1, 0, 1, 2]


def test_numpy_sum_shared(shared_data):
    assert np.sum(shared_data) == pytest.approx(15, abs=1e-3)


def test_numpy_cumsum_shared(shared_data):
    assert np.cumsum(shared_data) == pytest.approx([1, 3, 6, 10, 15], abs=1e-3)


def test_numpy_sum_local(local_data):
    assert np.sum(local_data) == pytest.approx(0, abs=1e-3)


def test_numpy_cumsum_local(local_data):
    assert np.cumsum(local_data) == pytest.approx([-2, -3, -3, -2, 0], abs=1e-3)
