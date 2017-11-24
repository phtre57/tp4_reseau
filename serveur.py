#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketUtil import recv_msg, send_msg
import socket, optparse, sys
import re
import os
import errno
from hashlib import sha256

class Server:

    def __init__(self):
        self.destination = ("localhost", 1337)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(self.destination)
        self.serversocket.listen(5)
        print("Listening on port " + str(self.serversocket.getsockname()[1]))

        self.__listenForConnexion()

    def __listenForConnexion(self):
        i = 0
        while True:
            (s, address) = self.serversocket.accept()
            i += 1
            print(str(i) + " connexion to server")
            self.__listen(s)

    def __listen(self, s):
        try:
            operation = recv_msg(s)

            if operation == str(1):
                self.__connexion(s)

            elif operation == str(2):
                self.__createUser(s)
        except Exception as ex:
            print(ex)


    def __connexion(self, s):
        username = recv_msg(s)
        password = recv_msg(s)
        hashedPassword = sha256(password.encode()).hexdigest()
        filename = "./" + username + "/config.txt"
        if os.path.exists(os.path.dirname(filename)):
            try:
                with open(filename, "r") as file:
                    readPassword = file.readline();
                    if str(hashedPassword) == str(readPassword):
                        send_msg(s, "passwordOk")
                    else:
                        send_msg(s, "passwordWrong")
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    send_msg(s, "race condition")
        else:
            send_msg(s, "notExistUsername")


        self.__listen(s)

    def __createUser(self, s):
        username = recv_msg(s)
        password = recv_msg(s)
        hashedPassword = ""
        if re.search(r"^(?=.*\d)(?=.*[a-zA-Z]).{6,12}$", password):
            hashedPassword = sha256(password.encode()).hexdigest()
        else:
            send_msg(s, "incorrectPassword")

        filename = "./" + username + "/config.txt"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    send_msg("race condition")

            with open(filename, "w") as file:
                file.write(hashedPassword)
            send_msg(s, "userCreated")
        else:
            send_msg(s, "usernameExists")

        self.__listen(s)



newServer = Server()

