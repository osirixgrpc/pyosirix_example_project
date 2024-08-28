""" An example test file to demonstrate local fixture sharing. """

import pytest
import numpy as np


@pytest.fixture(scope="function")
def local_data():
    """ This fixture can only be used in this module. """
    yield [-2, -1, 0, 1, 2]


def test_numpy_sum_shared(shared_data):
    assert pytest.approx(np.sum(shared_data), 15, abs=1e-3)


def test_numpy_cumsum_shared(shared_data):
    assert pytest.approx(np.cumsum(shared_data), [1, 3, 6, 10, 15], abs=1e-3)


def test_numpy_sum_local(local_data):
    assert pytest.approx(np.sum(local_data), 0, abs=1e-3)


def test_numpy_cumsum_local(local_data):
    assert pytest.approx(np.cumsum(local_data), [-2, -3, -3, -2, 0], abs=1e-3)
