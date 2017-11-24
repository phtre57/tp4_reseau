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

        self.showConnexionMenu()

    def showConnexionMenu(self):
        choice = input("Menu de connexion \n 1. Se connecter \n 2. Creer un compte \n")

        if choice == 1 or choice == str(1):
            self.__connexionToServer()

        elif choice == 2 or choice == str(2):
            self.__createUser()

        else:
            print("Choix invalide")
            self.showConnexionMenu()

    def __connexionToServer(self):
        self.username = input("Entrez votre nom d'usager: ")
        self.password = getpass.getpass("Entrez votre mot de passe: ")

        send_msg(self.s, str(1))
        send_msg(self.s, self.username)
        send_msg(self.s, self.password)

        self.showMainMenu()

    def __createUser(self):
        self.username = input("Entrez le nom d'usager voulu: ")
        self.__createPassword()

    def __createPassword(self):
        self.password = input("Entrez le mot de passe voulu, il doit contenir entre 6 et 12 carateres dont au moins"
                              "une lettre et un chiffre: ")

        if re.search(r"^(?=.*\d)(?=.*[a-zA-Z]).{6,12}$", self.password):
            send_msg(self.s, str(2))
            send_msg(self.s, self.username)
            send_msg(self.s, self.password)
        else:
            print("Le mot de passe ne contient pas entre 6-12 caracteres ou au moins une lettre et un chiffre")
            self.__createPassword()

    def showMainMenu(self):
        choice = input("Menu principal \n 1. Envoie de courriel \n 2. Consultation de courriels \n "
                       "3. Statistiques \n 4. Quitter \n")


newClient = Client()