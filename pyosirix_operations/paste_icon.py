import os

import osirix
import numpy as np
from numpy.typing import NDArray
from PIL import Image
from skimage.transform import resize


class PasteIcon:
    """ Used to paste an icon in the current Viewer Controller
    """
    def __init__(self, icon_file: str = "icon.png"):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(current_path, icon_file)

    def read_icon(self, in_2d: bool = True) -> NDArray:
        """ Return a 2D NDArray representing the array of the icon file.

        Args:
            in_2d (bool): If True, the icon will be converted to a 2D NDArray (red channel).

        Returns:
            NDArray: The icon as an array.
        """
        if not os.path.exists(self.icon_path):
            raise FileNotFoundError("Could not find the icon file.")
        rgba = Image.open(self.icon_path).convert("RGBA")
        rgb_array = np.array(rgba)[..., 0:-1]
        if in_2d:
            rgb_array = rgb_array[..., 0]
        return rgb_array

    @staticmethod
    def paste_icon_in_array(icon: NDArray, array: NDArray, scale: float = 0.5)\
            -> NDArray:
        """ Apply a shape scaling to an array and add it to another.

        Args:
            icon (NDArray): The icon to add.
            array (NDArray): Array to paste within.
            scale (float): The scale for each dimension.

        Returns:
            NDArray: Array added.
        """
        if scale <= 0.0 or scale > 1.0:
            raise ValueError("Scale must be between 0 and 1.")

        if icon.ndim != array.ndim:
            raise ValueError("Arrays must have the same dimensions.")

        if icon.ndim not in [2, 3]:
            raise ValueError("Arrays must have dimension 2 or 3.")

        if icon.ndim == 3:
            if array.shape[-1] != 3 or icon.shape[-1] != 3:
                raise ValueError("3D arrays must have 3 channels in last dimension")

        scaled_shape = [int(sh * scale) for sh in array.shape[0:2]]
        if icon.ndim == 3:
            scaled_shape.append(3)
            scaled_icon = resize(icon, scaled_shape)
            array[0:scaled_shape[0], 0:scaled_shape[1], :] = scaled_icon
        else:
            scaled_icon = resize(icon, scaled_shape)
            array[0:scaled_shape[0], 0:scaled_shape[1]] = scaled_icon

        return array

    def pyosirix_add_icon_to_displayed_image(self):
        """ Add the icon to the top-left corner of the displayed image.
        """
        vc = osirix.frontmost_viewer()
        if vc is None:
            raise ValueError("No viewer displayed.")
        pix = vc.cur_dcm()
        current_array = pix.image
        if pix.is_rgb:
            icon = self.read_icon(in_2d=False)
        else:
            icon = self.read_icon(in_2d=True)
            icon = icon.astype("float32") / 255 * np.max(current_array)
        print(current_array.shape)
        new_array = self.paste_icon_in_array(icon, current_array, scale=0.1)
        print(new_array.shape)
        pix.image = new_array
        vc.needs_display_update()

    def run(self):
        """ Run the class. """
        self.pyosirix_add_icon_to_displayed_image()


if __name__ == "__main__":
    pu = PasteIcon()
    pu.run()
