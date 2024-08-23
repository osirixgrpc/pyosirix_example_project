import pytest

from pyosirix_example.utilities.text_2_image import Text2Image


@pytest.fixture(scope="function")
def text2image_instance():
    yield Text2Image()