import argparse
from irc_code import patterns
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread


class Client(patterns.Subscriber):

    def __init__(self, sock, address):
        self.sock = sock
        self.address = address[0]
        self.nickname = None
        self.username = None
        self.channel = channels[0]

    def update(self, msg):
        self.send(msg)

    def recv(self):
        return self.sock.recv(BUFFER_SIZE).decode('utf8')

    def send(self, msg, ):
        try:
            self.sock.send(bytes(f'{msg}', 'utf8'))
        except Exception:
            pass


class Channel(patterns.Publisher):

    def __init__(self, name):
        super().__init__()
        self.name = name


def get_client(client, username):
    client.username = username
    client.send('Username set to ' + username + '.')


def remove_client(client):
    if not client.nickname is None:
        client.send('Goodbye ' + client.nickname + '!')
    client.sock.close()

    if client in clients:
        clients.remove(client)


def edit_nickname(client, nickname):
    # Verifying that the nickname conforms to proper naming standards
    if ' ' in nickname or len(nickname) > 9 or not nickname[0].isalpha():
        client.send('Error: Your nickname must start with a letter following potentially more letters or '
                  'numbers or digits and no spaces with a max of 9 characters. Please retry.')

    # Checking to see if nickname is not taken
    elif nickname in [client.nickname for client in clients]:
        client.send('Error(ERR_NICKCOLLISION): ERR_NICKNAMEINUSE')
    # Setting the new nickname
    else:
        previous_nickname = client.nickname
        client.nickname = nickname
        client.send('Nickname changed to ' + nickname + '.')
        if previous_nickname is not None:
            client.channel.notify(
                f'{previous_nickname} now identifies themselves as {nickname}')


def irc_server_listen():
    while True:
        client, client_address = server.accept()
        current_client = Client(client, client_address)
        clients.append(current_client)

        print(current_client.address + ' has connected.')
        Thread(target=manage_socket_connection, args=(current_client,)).start()


def manage_socket_connection(client):
    client.channel.add_subscriber(client)
    client.send('Welcome to channel: #global')
    while True:

        # If the connection has been lost, properly kill delete the user and stop the loop.
        try:
            msg = client.recv()
            print(msg)
        except Exception:
            print(client.address + ' has been now closed by the server side.')
            remove_client(client)
            break

        if "/NICK " in msg:
            res = msg.split("/NICK ")[1]
            edit_nickname(client, res)

        elif "/USER " in msg:
            res = msg.split("/USER ")[1]
            get_client(client, res)

        elif "/QUIT " in msg:
            print(f'{client.address} has disconnected')
            remove_client(client)
            break

        elif msg:
            try:
                client.channel.notify(msg)
            except Exception:
                print(client.address + ' caused exception.')
                remove_client(client)
                break


def parse_args(args):
    parser = argparse.ArgumentParser(description='CLI for the server')
    parser.add_argument('--port', required=True,
                        help='Port for the server')
    return parser.parse_args(args)


clients = []
channels = [Channel('#global')]
args = parse_args(None)
HOST = ''
PORT = int(args.port)  # 50007
BUFFER_SIZE = 512  # "these messages shall not exceed 512 characters in length"

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(15)

print('The server is up and running. Waiting for Clients to connect via sockets')
thread = Thread(target=irc_server_listen)
thread.start()
thread.join()
server.close()
