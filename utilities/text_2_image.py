from typing import Tuple

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from numpy.typing import NDArray


class Text2Image:
    """ A class that creates a text image from a text string.

    Properties:
        max_shape (Tuple[int, int]): The maximum shape of the initial text image. Set to something
            large to avoid text clipping. Default is (5000, 5000).
    """
    def __init__(self, max_shape: Tuple[int, int] = None):
        self.max_shape = max_shape

    def text_to_image_array(self, text: str, font_path: str = None, font_size: int = 40) -> NDArray:
        """ Convert a text string into an image.

        Args:
            text (str): The text to be converted.
            font_path (str, optional): A path to a font file. Defaults to None in which case it is
                handled by PIL.
            font_size (int, optional): A font size. Defaults to 40.

        Returns:
            NDArray: The text image.
        """
        img = Image.new('L', self.max_shape, 0)  # 'L' mode: 0 = black, 255 = white.
        draw = ImageDraw.Draw(img)

        # Optional: Load a font, otherwise it will use the default font
        if font_path:
            font = ImageFont.truetype(font_path, font_size)
        else:
            font = ImageFont.load_default(font_size)

        # Add text to the image
        draw.text((0, 0), text, fill=255, font=font)

        # Convert the image to a numpy array
        img_array = np.array(img)

        # Remove un-needed rows/columns
        x, y = np.where(img_array > 0)
        img_array = img_array[np.min(x):np.max(x),
                              np.min(y):np.max(y)]

        # Return the binary image array
        return img_array

    def text_to_mask_array(self, text: str, font_path: str = None, font_size: int = 40,
                           threshold: int = 100) -> NDArray:
        """ Convert a text string into an image.

        Args:
            text (str): The text to be converted.
            font_path (str, optional): A path to a font file. Defaults to None in which case it is
                handled by PIL.
            font_size (int, optional): A font size. Defaults to 40.
            threshold (int, optional): A threshold between 0 and 255 for creating a mask.
                Defaults to 100.

        Returns:
            NDArray: The binary text mask.
        """
        img_array = self.text_to_image_array(text, font_path, font_size)
        return img_array > threshold
