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

    def start_server(self):
        """ Start the server.
        """
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),
                                  options=[("grpc.max_receive_message_length",
                                            self.max_receive_message_length),
                                           ("grpc.max_send_message_length",
                                            self.max_send_message_length)]
                                  )
        service_pb2_grpc.add_PyosirixExampleServiceServicer_to_server(PyosirixExampleService(),
                                                                      self.server)
        self.server.add_insecure_port(f'{self.domain}:{self.port}')
        self.server.start()
        print(f"Server is running on {self.domain}:{self.port}...")
        self.server.wait_for_termination()


if __name__ == "__main__":
    Server().start_server()
