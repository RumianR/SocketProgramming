# Echo client program
import socket
import argparse
import sys
from threading import Thread



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

def recv(server_socket, buffer_size):
    # If the connection is lost, properly stop the program.
    CONNECTED = True

    while CONNECTED:
        try:
            datarecv = server_socket.recv(buffer_size).decode('utf8')
            if datarecv == "":
                raise Exception
            print(f'{HOST}:', repr(datarecv))

        except Exception:
            print('The connection with the server has been lost')
            CONNECTED = False
            server_socket.close()
            sys.exit()
            break


args = parse_args(None)
HOST = args.server
PORT = int(args.port)
NAME = args.name
NICKNAME = args.nickname
BUFFER_SIZE = 512

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     data = s.recv(1024)
# print('Received', repr(data))
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
CONNECTED = True
Thread(target=recv, args=(socket, BUFFER_SIZE,)).start()
socket.send(bytes(f'{NICKNAME}: /NICK {NICKNAME}', 'utf8')) #THIS RETURNS NONE FOR SOME REASON


while True:
    try:
        data = sys.stdin.readline()[:-1]
        data = f':{NICKNAME} {data}'
    except Exception:
        exit()
    socket.sendall(bytes(data, 'utf8'))

    if "/QUIT " in data:
        exit()

    # print(f'{NAME} sent', repr(data))

