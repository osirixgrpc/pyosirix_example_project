""" An example configuration file to demonstrate package-wide fixture sharing. """

import pytest


@pytest.fixture(scope='function')
def shared_data():
    """ Example fixture, yielding test data shared across all test files in this directory.
    """
    yield [1, 2, 3, 4, 5]
