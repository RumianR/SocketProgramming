#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021
#
# Distributed under terms of the MIT license.

"""
Description:

"""
import asyncio
import logging
from socket import AF_INET, socket, SOCK_STREAM
from irc_code import patterns
from irc_code import view


logging.basicConfig(filename='view.log', level=logging.DEBUG)
logger = logging.getLogger()
client_socket = socket(AF_INET, SOCK_STREAM)
server_connected = False


class IRCClient(patterns.Subscriber):

    def __init__(self):
        super().__init__()
        self.username = str()
        self.nickname = str()
        self._run = True

    def set_view(self, view):
        self.view = view

    def update(self, msg):
        # Will need to modify this
        if not isinstance(msg, str):
            raise TypeError(f"Update argument needs to be a string")
        elif not len(msg):
            # Empty string
            return
        logger.info(f"IRCClient.update -> msg: {msg}")
        self.process_input(msg)

    def process_input(self, msg):
        # Will need to modify this
        if not server_connected:

            if not self.nickname:
                if msg.startswith("nickname:"):
                    self.nickname = msg.split(":")[1]
                    self.add_msg(f"Got it nickname is {self.nickname}")
                else:
                    self.add_msg("Please enter nickname in the format 'nickname:<nickname>'")
                return
            # if not self.username and self.nickname:
            #     if msg.startswith("username:"):
            #         self.username = msg.split(":")[1]
            #         self.add_msg(f"Got it username is {self.username}")
            #         self.add_msg("Connecting")
            #         conn_server()
            #         Thread(target=recv, args=(client_socket, BUFFER_SIZE, self,)).start()
            #     else:
            #         self.add_msg("Please enter username in the format 'username:<username>'")
            #     return

        self.add_msg(msg)

        try:
            client_socket.send(bytes(msg, 'utf8'))
        except Exception:
            logger.error("Could not send msg")

        if msg.lower().startswith('/quit'):
            # Command that leads to the closure of the process
            raise KeyboardInterrupt

    def add_msg(self, msg):
        self.view.add_msg(self.username, msg)

    async def run(self):
        """
        Driver of your IRC Client
        """

    def close(self):
        # Terminate connection

        logger.debug(f"Closing IRC Client object")
        pass


def main(args):
    # Pass your arguments where necessary

    client = IRCClient()
    logger.info(f"Client object created")

    with view.View() as v:
        logger.info(f"Entered the context of a View object")
        client.set_view(v)
        logger.debug(f"Passed View object to IRC Client")
        v.add_subscriber(client)
        logger.debug(f"IRC Client is subscribed to the View (to receive user input)")


        async def inner_run():
            await asyncio.gather(
                v.run(),
                client.run(),
                return_exceptions=True,
            )

        try:
            asyncio.run(inner_run())
        except KeyboardInterrupt as e:
            logger.debug(f"Signifies end of process")
    client.close()


if __name__ == "__main__":
    # Parse your command line arguments here
    args = None
    main(args)
