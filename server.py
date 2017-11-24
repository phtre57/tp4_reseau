#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketUtil import recv_msg, send_msg
import socket, optparse, sys
import re

class Server:

    def __init__(self):
        self.destination = ("localhost", 1337)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(self.destination)
        self.serversocket.listen(5)

        self.__listen()

    def __listen(self):
        print("Listening on port " + str(self.serversocket.getsockname()[1]))
        i = 0
        while True:
            (s, address) = self.serversocket.accept()
            i += 1
            print(str(i) + " connexion to server")
            operation = recv_msg(s)

            if operation == str(1):
                self.__connexion(s)

            elif operation == str(2):
                self.__createUser(s)

    def __connexion(self, s):
        username = recv_msg(s)
        password = recv_msg(s)
        print(username + ", " + password)

    def __createUser(self, s):
        username = recv_msg(s)
        password = recv_msg(s)
        if re.search(r"^(?=.*\d)(?=.*[a-zA-Z]).{6,12}$", password):
            print(username + ", " + password)



newServer = Server()

