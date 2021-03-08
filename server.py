# Echo server program
from socket import AF_INET, socket, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread

from irc_code import patterns
import argparse


class Channel(patterns.Publisher):

    def __init__(self, name):
        super().__init__()
        self.name = name


class User(patterns.Subscriber):

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

    def send(self, msg,):
        try:
            self.sock.send(bytes(f'{msg}', 'utf8')) #THIS RETURNS NONE FOR SOME REASON
        except Exception:
            pass


def get_user(nickname):
    for user in users:
        if user.nickname == nickname:
            return user


def edit_nickname(user, nickname):
    if ' ' in nickname or len(nickname) > 9 or not nickname[0].isalpha():
        user.send('Error: Your nickname must start with a letter following potentially more letters or '
                  'numbers or digits and no spaces with a max of 9 characters. Please retry.')

    # Make sure the nickname isn't already use
    elif nickname in [user.nickname for user in users]:
        user.send('Error: ERR_NICKNAMEINUSE')

    else:
        previous_nickname = user.nickname
        user.nickname = nickname
        user.send('Nickname changed to ' + nickname + '.')
        if previous_nickname is not None:
            user.channel.notify(
                f'{previous_nickname} now identifies themselves as {nickname}')


def edit_user(user, username):
    # It must be noted that realname parameter must be the last parameter,
    # because it may contain space characters
    # and must be prefixed with acolon (':') to make sure this is recognised as such.
    user.username = username
    user.send('Username set to ' + username + '.')


def remove_user(user):
    # if not user.nickname is None:
    #     user.send('Goodbye ' + user.nickname + '!')

    user.sock.close()

    if user in users:
        users.remove(user)


def irc_server_listen():
    while True:
        client, client_address = server.accept()
        user = User(client, client_address)
        users.append(user)

        print(user.address + ' has connected.')
        Thread(target=manage_socket_connection, args=(user,)).start()


def manage_socket_connection(user):
    # import pdb; pdb.set_trace()
    user.channel.add_subscriber(user)
    user.send('Welcome to channel: #global')
    while True:

        # If the connection has been lost, properly kill delete the user and stop the loop.
        try:
            msg = user.recv()
            print(msg)
        except Exception:
            print(user.address + ' was forcibly closed by the remote host.')
            remove_user(user)
            break

        if "/NICK " in msg:
            res = msg.split("/NICK ")[1]
            edit_nickname(user, res)

        elif "/USER " in msg:
            res = msg.split("/USER ")[1]
            edit_user(user, res)

        elif "/QUIT " in msg:
            print(f'{user.address} has disconnected')
            # import pdb; pdb.set_trace()
            remove_user(user)
            break

        elif msg:
            try:
                # import pdb; pdb.set_trace()
                user.channel.notify(msg)
            except Exception:
                print(user.address + ' caused exception.')
                remove_user(user)
                break

def parse_args(args):
    parser = argparse.ArgumentParser(description='CLI for the server')
    parser.add_argument('--port', required=True,
                        help='Port for the server')
    return parser.parse_args(args)

users = []
channels = [Channel('#global')]

args = parse_args(None)
HOST = ''  # Symbolic name meaning all available interfaces
PORT = int(args.port)
# PORT = 50007  # Arbitrary non-privileged port
BUFFER_SIZE = 512  # "these messages shall not exceed 512 characters in length"

server = socket(AF_INET, SOCK_STREAM)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind((HOST, PORT))

server.listen(10)

print('The server has succefully launched. Now waiting for client connection...')
thread = Thread(target=irc_server_listen)
thread.start()
thread.join()
server.close()
