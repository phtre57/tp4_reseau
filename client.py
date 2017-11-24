#!/usr/bin/env python
# -*- coding: utf-8 -*-
from socketUtil import recv_msg, send_msg
import socket, optparse, sys
import getpass
import re


class Client:

    def __init__(self):
        self.username = ""
        self.password = ""
        self.destination = ("localhost", 1337)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(self.destination)

        self.__showConnexionMenu()

    def __showConnexionMenu(self):
        choice = input("Menu de connexion \n 1. Se connecter \n 2. Creer un compte \n")

        if choice == 1 or choice == str(1):
            self.__connexionToServer()

        elif choice == 2 or choice == str(2):
            self.__createUser()

        else:
            print("Choix invalide")
            self.__showConnexionMenu()

    def __connexionToServer(self):
        self.username = input("Entrez votre nom d'usager: ")
        self.password = getpass.getpass("Entrez votre mot de passe: ")

        send_msg(self.s, str(1))
        send_msg(self.s, self.username)
        send_msg(self.s, self.password)

        try:
            message = recv_msg(self.s)

            if message == "passwordOk":
                self.__showMainMenu()

            elif message == "passwordWrong":
                print("Mauvais mot de passe")
                self.__connexionToServer()

            elif message == "notExistUsername":
                print("Le nom d'usage rentrer ne correspond a aucun usage")
                self.__connexionToServer()

            else:
                print("Probleme au niveau du serveur: " + message)
                self.__connexionToServer()
        except Exception as ex:
            print(ex)


    def __createUser(self):
        self.username = input("Entrez le nom d'usager voulu: ")
        self.__createPassword()

    def __createPassword(self):
        self.password = getpass.getpass("Entrez le mot de passe voulu, il doit contenir entre 6 et 12 carateres dont au moins"
                              "une lettre et un chiffre: ")

        if re.search(r"^(?=.*\d)(?=.*[a-zA-Z]).{6,12}$", self.password):
            send_msg(self.s, str(2))
            send_msg(self.s, self.username)
            send_msg(self.s, self.password)
        else:
            print("Le mot de passe ne contient pas entre 6-12 caracteres ou au moins une lettre et un chiffre")
            self.__createPassword()

        try:
            message = recv_msg(self.s)
            if message == "userCreated":
                print("Usage cree")
                self.__showMainMenu()
            elif message == "usernameExists":
                print("Usage existe deja veuillez choisir un autre nom d'usage")
                self.__createUser()
            elif message == "incorrectPassword":
                self.__createPassword()
            else:
                print("Probleme au niveau du serveur: " + message)
                self.__showConnexionMenu()
        except Exception as ex:
            print(ex)


    def __showMainMenu(self):
        print("Bienvenue: " + self.username)
        choice = input("Menu principal \n 1. Envoie de courriel \n 2. Consultation de courriels \n "
                       "3. Statistiques \n 4. Quitter \n")

        if choice == str(1) or choice == 1:
            self.__sendMail()
            self.__showMainMenu()
        elif choice == str(2) or choice == 2:
            print(2)
            self.__showMainMenu()
        elif choice == str(3) or choice == 3:
            print(3)
            self.__showMainMenu()
        elif choice == str(4) or choice == 4:
            self.username = ""
            self.password = ""
            self.__showConnexionMenu()
        else:
            print("Choix invalide")
            self.__showMainMenu()

    def __sendMail(self):
        dest = self.__destOk()
        subject = input("Entrez le sujet: ")
        message = input("Entrez le message: ")

        send_msg(self.s, str(3))
        send_msg(self.s, dest)
        send_msg(self.s, subject)
        send_msg(self.s, message)
        send_msg(self.s, self.username + "@reseauglo.ca")

        try:
            message = recv_msg(self.s)
            print(message)
        except Exception as ex:
            print(ex)

    def __destOk(self):
        dest = input("Entrez le destinataire: ")
        if re.search(r"[^@]+@[^@]+\.[^@]", dest):
            return dest
        else:
            print("Rentrez un email valide (ex: exemple@gmail.com)")
            self.__destOk()






newClient = Client()