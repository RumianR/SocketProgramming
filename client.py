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
            print(f'{HOST} (empty message):', repr(datarecv))

        except Exception:
            print('Lost server connection')
            # close socket and exit the system
            server_socket.close()
            sys.exit()
            break


args = parse_args(None)
HOST = args.server
PORT = int(args.port)
NAME = args.name
NICKNAME = args.nickname
# IRC messages shall not exceed 512 characters in length
BUFFER_SIZE = 512

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((HOST, PORT))
CONNECTED = True
Thread(target=recv, args=(socket, BUFFER_SIZE,)).start()
socket.send(bytes(f'{NICKNAME}: /NICK {NICKNAME}', 'utf8'))


while True:
    try:
        data = input()
        data = f':{NICKNAME} {data}'
    except Exception:
        exit()
    socket.sendall(bytes(data, 'utf8'))

    if "/QUIT " in data:
        exit()
