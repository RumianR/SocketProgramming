# Echo client program
import socket
import argparse
import sys


def parse_args(args):
    parser = argparse.ArgumentParser(description='CLI for the client')
    parser.add_argument('--server', required=True,
                        help='Server for the client')
    parser.add_argument('--port', required=True,
                        help='Port for the client')
    parser.add_argument('--name', required=True,
                        help='Name for the client')
    parser.add_argument('--nickname', required=True,
                        help='Nickname for the client')
    return parser.parse_args(args)


args = parse_args(None)
HOST = args.server
PORT = int(args.port)
NAME = args.name
NICKNAME = args.nickname

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
# print('Received', repr(data))
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))

while True:
    try:
        data = sys.stdin.readline()[:-1]
    except Exception:
        exit()
    socket.sendall(bytes(data, 'utf8'))

    print(f'{NAME} sent', repr(data))