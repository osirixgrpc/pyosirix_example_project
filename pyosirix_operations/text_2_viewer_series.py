import osirix
from numpy.typing import NDArray

from utilities.text_2_image import Text2Image


class Text2Viewer:
    """ Burn text to images on an OsiriX viewer controller.
    """
    

    def run(self):
        return 0


# There should be at least one "hook" file that runs during execution of the script.
if __name__ == '__main__':
    t2v = Text2Viewer()
    t2v.run()
