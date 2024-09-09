""" Implements the service defined in the service.proto file. """
import numpy as np

from pyosirix_example.server.data_loader import DataLoader
from pyosirix_example.grpc_protocols import service_pb2, service_pb2_grpc
from pyosirix_example.utilities.text_2_image import Text2Image


class PyosirixExampleService(service_pb2_grpc.PyosirixExampleServiceServicer):
    def __init__(self):
        self.data_loader = DataLoader()

    def ProcessImage(self, request, context):

        # Convert to numpy array
        array = np.array(request.image).reshape(request.rows, request.columns)

        # Get the data to add
        text = self.data_loader.data

        # Process the image
        t2i = Text2Image()
        new_array = t2i.paste_text_in_array(text,
                                            array,
                                            location=3,  # Top left
                                            scale=0.75,
                                            offset=0.05,
                                            remove_background=False,
                                            align="left",
                                            font_path="GillSans.ttc",
                                            value=4095,
                                            bg_value=0)

        # Create a list
        flat_list = new_array.ravel().tolist()

        # Return the processed image
        return service_pb2.Image(rows=request.rows, columns=request.columns, image=flat_list)
