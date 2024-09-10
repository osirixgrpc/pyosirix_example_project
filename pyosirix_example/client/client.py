import os

import osirix
from osirix.dcm_pix import DCMPix
from osirix.viewer_controller import ViewerController
import grpc
import numpy as np

from pyosirix_example.grpc_protocols import service_pb2_grpc
from pyosirix_example.grpc_protocols import service_pb2


class Client:
    """ Burn text to images on an OsiriX viewer controller.

    Attributes:
        domain (str): The domain of the server. Default is "127.0.0.1" (localhost).
        port (int): The port number with which to establish the connection. Default is 50051.
        max_send_message_length (int): The maximum number of bytes permitted in a send message.
            Default is 500000000 (500 MB).
        max_receive_message_length (int): The maximum number of bytes permitted in a receive
            message. Default is 500000000 (500 MB).
    """
    def __init__(self, domain: str = "127.0.0.1", port: int = 50051,
                 max_send_message_length: int = 512 * 1024 * 1024,
                 max_receive_message_length: int = 512 * 1024 * 1024):
        self.port = port
        self.domain = domain
        self.server_url = domain + ":" + str(self.port)
        self.max_send_message_length = max_send_message_length
        self.max_receive_message_length = max_receive_message_length
        self.service_stub = None
        self.channel = None
        self.start_connection()

    def client_certificates_path(self) -> str:
        """ Returns the expected certificates path of this client.

        Returns:
            str: The path to the certificate's directory.
        """
        return os.path.join(os.path.expanduser("~"), "certs", "pyosirix", "client", self.domain)

    def ca_certificate(self) -> bytes:
        """ Return the ca certificate for the machine running this script.
        """
        cert_path = os.path.join(self.client_certificates_path(), "ca.crt")
        if not os.path.exists(cert_path):
            raise FileNotFoundError("No ca certificate found for this client. "
                                    "Please run `client_server_certs.sh`")

        with open(cert_path, "rb") as cert_file:
            cert = cert_file.read()
        return cert

    def client_certificate(self) -> bytes:
        """ Return the client certificate for the machine running this script.
        """
        cert_path = os.path.join(self.client_certificates_path(), "client.crt")
        if not os.path.exists(cert_path):
            raise FileNotFoundError("No client certificate found for this client. "
                                    "Please run `client_server_certs.sh`")

        with open(cert_path, "rb") as cert_file:
            cert = cert_file.read()
        return cert

    def client_key(self) -> bytes:
        """ Return the client key for the machine running this script.
        """
        key_path = os.path.join(self.client_certificates_path(), "client.key")
        if not os.path.exists(key_path):
            raise FileNotFoundError("No client key found for this client. "
                                    "Please run `client_server_certs.sh`")

        with open(key_path, "rb") as cert_file:
            key = cert_file.read()
        return key

    def start_connection(self):
        """ Start the insecure client service.

        Raises:
            GrpcException: Occurs when something goes wrong trying to set up the connection.

        """
        key = self.client_key()
        cert = self.client_certificate()
        ca_cert = self.ca_certificate()
        credentials = grpc.ssl_channel_credentials(root_certificates=ca_cert,
                                                   private_key=key,
                                                   certificate_chain=cert)

        # Create a secure gRPC channel
        self.channel = grpc.secure_channel(self.server_url,
                                           credentials,
                                           options=[("grpc.max_receive_message_length",
                                                    self.max_receive_message_length),
                                                    ("grpc.max_send_message_length",
                                                    self.max_send_message_length)])

        self.service_stub = service_pb2_grpc.PyosirixExampleServiceStub(self.channel)

    def stop_connection(self):
        """ Stop the insecure client service. """
        if self.channel:
            self.channel.close()

    def write_text_in_pix(self, pix: DCMPix) -> None:
        """ Write a text string in an OsiriX DCMPix instance.

        Args:
            pix (DCMPix): The OsiriX DCMPix.
        """
        if pix.is_rgb:
            raise ValueError("This project does not yet support RGB images.")

        # Get the image array
        image_array = pix.image

        # Convert to a flattened list
        image_list = image_array.ravel().tolist()

        # Create the "Image" message to send to the server
        image = service_pb2.Image(rows=image_array.shape[0],
                                  columns=image_array.shape[1],
                                  image=image_list)

        # Call the service
        response = self.service_stub.ProcessImage(image)

        # Recreate the returned image array
        new_image_array = np.array(response.image).reshape(response.rows, response.columns)

        # Put the new data into the pix object
        pix.image = new_image_array.astype("float32")

    def write_text_in_viewer_controller(self, viewer: ViewerController, movie_idx: int = -1)\
            -> None:
        """ Write a text string in all DCMPix instances within a viewer.

        Args:
            viewer (ViewerController): The OsiriX ViewerController.
            movie_idx (int): The frame of the viewer in which to write the text. Default is -1 in
                which case all frames are written.
        """
        if movie_idx == -1:
            for idx in range(viewer.max_movie_index):
                pix_list = viewer.pix_list(idx)
                for pix in pix_list:
                    self.write_text_in_pix(pix)
        else:
            pix_list = viewer.pix_list(movie_idx)
            for pix in pix_list:
                self.write_text_in_pix(pix)
        viewer.needs_display_update()

    def write_text_in_selected_viewer_controller(self) -> None:
        """ Write a text string in all DCMPix instances within the user-selected viewer.
        """
        viewer = osirix.frontmost_viewer()
        self.write_text_in_viewer_controller(viewer)

    def run(self):
        self.write_text_in_selected_viewer_controller()


# How to run the client.
if __name__ == '__main__':
    # You could process arguments here.
    Client().run()
