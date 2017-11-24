#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketUtil import recv_msg, send_msg
import socket, optparse, sys
import re
import os
import errno
from hashlib import sha256
import smtplib
from email.mime.text import MIMEText

class Server:

    def __init__(self):
        self.destination = ("localhost", 1337)
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind(self.destination)
        self.serversocket.listen(5)
        print("Listening on port " + str(self.serversocket.getsockname()[1]))
        filename = "./DESTERREUR"
        if not os.path.exists(filename):
            try:
                os.makedirs(filename)
            except OSError as ex:
                if ex.errno != errno.EEXIST:
                    print(ex)
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
            operation = str(recv_msg(s))

            #1 connexion user
            if operation == str(1):
                self.__connexion(s)

            #2 creation user
            elif operation == str(2):
                self.__createUser(s)

            #3 send mail
            elif operation == str(3):
                self.__sendMail(s)

        except Exception as ex:
            print(ex)


    def __connexion(self, s):
        try:
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
        except Exception as ex:
            print(ex)

        self.__listen(s)

    def __createUser(self, s):
        try:
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
        except Exception as ex:
            print(ex)

        self.__listen(s)

    def __sendMail(self, s):
        try:
            dest = recv_msg(s)
            subject = recv_msg(s)
            message = recv_msg(s)
            username = recv_msg(s)

            if re.search(r".+@reseauglo\.ca", dest):
                dest1, dest2 = dest.split("@")
                filename = "./" + dest1
                if os.path.exists(filename):
                    try:
                        os.makedirs(os.path.dirname(filename + "/" + subject + ".txt"))

                    except OSError as ex1:
                        if ex1.errno != errno.EEXIST:
                            send_msg(s, "race condition")
                            print(ex1)

                    with open(filename + "/" + subject + ".txt", "w") as file:
                        file.write(message)
                        send_msg(s, "mailOk")

                else:
                    try:
                        os.makedirs(os.path.dirname("DESTERREUR/" + subject + ".txt"))

                    except OSError as ex1:
                        if ex1.errno != errno.EEXIST:
                            send_msg(s, "race condition")
                            print(ex1)

                    with open("DESTERREUR/" + subject + ".txt", "w") as file:
                        file.write(message)
                        send_msg(s, "noDest")

            else:
                msg = MIMEText(message)
                msg["FROM"] = username
                msg["TO"] = dest
                msg["Subject"] = subject
                try:
                    smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
                    smtpConnection.sendmail(username, dest, msg.as_string())
                    smtpConnection.quit()
                    send_msg(s, "otherDest")
                except Exception as ex2:
                    send_msg(s, ex2)

        except Exception as ex:
            print(ex)

        self.__listen(s)



newServer = Server()

