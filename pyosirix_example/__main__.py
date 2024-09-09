import argparse

from pyosirix_example.server import server
from pyosirix_example.client import client


def run_server(ip_address: str = '127.0.0.1', port: int = 50051):
    print(f"Starting server on {ip_address}:{port}")
    server.Server(domain=ip_address, port=port).start_server()


def run_client(ip_address='127.0.0.1', port=50051):
    print(f"Connecting to server at {ip_address}:{port}")
    client.Client(domain=ip_address, port=port).run()


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Run in either server or client mode")

    # Add arguments
    parser.add_argument('--mode', choices=['server', 'client'], required=True,
                        help='Mode to run: "server" or "client"')
    parser.add_argument('--ip_address', type=str, default='127.0.0.1',
                        help='IP address to use (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=50051,
                        help='Port to use (default: 50051)')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Determine mode and execute corresponding function
    if args.mode == 'server':
        run_server(ip_address=args.ip_address, port=args.port)
    elif args.mode == 'client':
        run_client(ip_address=args.ip_address, port=args.port)


if __name__ == '__main__':
    main()
