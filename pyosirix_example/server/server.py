import os
from concurrent import futures

import grpc

from pyosirix_example.server.data_loader import DataLoader
from pyosirix_example.server.service import PyosirixExampleService
from pyosirix_example.grpc_protocols import service_pb2_grpc


class Server:
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
        self.data_loader = DataLoader()
        self.server = None

    @staticmethod
    def server_certificates_path() -> str:
        """ Returns the expected certificates path of this server.

        Returns:
            str: The path to the certificate's directory.
        """
        return os.path.join(os.path.expanduser("~"), "certs", "pyosirix", "server")

    def ca_certificate(self) -> bytes:
        """ Return the ca certificate for the machine running this script.
        """
        cert_path = os.path.join(self.server_certificates_path(), "ca.crt")
        if not os.path.exists(cert_path):
            raise FileNotFoundError("No ca certificate found for this server. "
                                    "Please run `client_server_certs.sh`")

        with open(cert_path, "rb") as cert_file:
            cert = cert_file.read()
        return cert

    def server_certificate(self) -> bytes:
        """ Return the server certificate for the machine running this script.
        """
        cert_path = os.path.join(self.server_certificates_path(), "server.crt")
        if not os.path.exists(cert_path):
            raise FileNotFoundError("No server certificate found for this server. "
                                    "Please run `client_server_certs.sh`")

        with open(cert_path, "rb") as cert_file:
            cert = cert_file.read()
        return cert

    def server_key(self) -> bytes:
        """ Return the server key for the machine running this script.
        """
        key_path = os.path.join(self.server_certificates_path(), "server.key")
        if not os.path.exists(key_path):
            raise FileNotFoundError("No server key found for this server. "
                                    "Please run `client_server_certs.sh`")

        with open(key_path, "rb") as cert_file:
            key = cert_file.read()
        return key

    def start_server(self):
        """ Start the server.
        """

        # Create server credentials using the server certificate and private key
        key = self.server_key()
        cert = self.server_certificate()
        ca_cert = self.ca_certificate()
        credentials = grpc.ssl_server_credentials([(key, cert)],
                                                  root_certificates=ca_cert,
                                                  require_client_auth=True)

        # Create a gRPC server
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                                  options=[("grpc.max_receive_message_length",
                                            self.max_receive_message_length),
                                           ("grpc.max_send_message_length",
                                            self.max_send_message_length)])

        # Add gRPC service to the server
        service_pb2_grpc.add_PyosirixExampleServiceServicer_to_server(PyosirixExampleService(),
                                                                      self.server)

        # Bind the server to a secure port using the credentials
        self.server.add_secure_port(f'{self.domain}:{self.port}', credentials)

        self.server.start()
        print(f"Server is running on {self.domain}:{self.port}...")

        self.server.wait_for_termination()


if __name__ == "__main__":
    Server().start_server()
