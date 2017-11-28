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
        try:
            choice = input("\nMenu de connexion\n1. Se connecter\n2. Creer un compte\n3. Quitter\n")

            if choice == 1 or choice == str(1):
                self.__connexionToServer()

            elif choice == 2 or choice == str(2):
                self.__createUser()

            elif choice == 3 or choice == str(3):
                self.s.close()

            else:
                print("Choix invalide")
                self.__showConnexionMenu()
        except Exception as ex:
            print(ex)

    def __connexionToServer(self):
        try:
            self.username = input("\nEntrez votre nom d'usager: ")
            self.password = getpass.getpass("Entrez votre mot de passe: ")

            send_msg(self.s, str(1))
            send_msg(self.s, self.username)
            send_msg(self.s, self.password)
        except Exception as ex:
            print(ex)

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
        try:
            self.username = input("\nEntrez le nom d'usager voulu: ")
            self.__createPassword()
        except Exception as ex:
            print(ex)


    def __createPassword(self):
        try:
            self.password = getpass.getpass("Entrez le mot de passe voulu, il doit contenir entre 6 et 12 carateres dont au moins"
                                  "une lettre et un chiffre: ")

            if re.search(r"^(?=.*\d)(?=.*[a-zA-Z]).{6,12}$", self.password):
                send_msg(self.s, str(2))
                send_msg(self.s, self.username)
                send_msg(self.s, self.password)
            else:
                print("Le mot de passe ne contient pas entre 6-12 caracteres ou au moins une lettre et un chiffre")
                self.__createPassword()
        except Exception as ex:
            print(ex)

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
        try:
            print("\nBienvenue: " + self.username)
            choice = input("Menu principal \n 1. Envoie de courriel \n 2. Consultation de courriels \n "
                           "3. Statistiques \n 4. Quitter \n")

            if choice == str(1) or choice == 1:
                self.__sendMail()
                self.__showMainMenu()
            elif choice == str(2) or choice == 2:
                self.__showMails()
                self.__showMainMenu()
            elif choice == str(3) or choice == 3:
                self.__showStats()
                self.__showMainMenu()
            elif choice == str(4) or choice == 4:
                self.username = ""
                self.password = ""
                self.__showConnexionMenu()
            else:
                print("Choix invalide")
                self.__showMainMenu()
        except Exception as ex:
            print(ex)

    def __sendMail(self):
        try:
            dest = self.__destOk()
            subject = input("Entrez le sujet: ")
            message = input("Entrez le message: ")

            send_msg(self.s, str(3))
            send_msg(self.s, dest)
            send_msg(self.s, subject)
            send_msg(self.s, message)
            send_msg(self.s, self.username + "@reseauglo.ca")
        except Exception as ex:
            print(ex)

        try:
            message = recv_msg(self.s)
            if message == "mailOk":
                print("Message envoyee!")
            elif message == "noDest":
                print("Destinataire non existant!")
            elif message == "otherDest":
                print("Message envoyee a un destinataire exterieur!")
        except Exception as ex:
            print(ex)

    def __destOk(self):
        dest = input("\nEntrez le destinataire: ")
        if re.search(r"[^@]+@[^@]+\.[^@]", dest):
            return dest
        else:
            print("Rentrez un email valide (ex: exemple@gmail.com)")
            self.__destOk()

    def __showMails(self):
        send_msg(self.s, str(4))
        send_msg(self.s, self.username)
        try:
            length = int(recv_msg(self.s)) + 1
            subjects = recv_msg(self.s)
            if subjects == "messageEmpty":
                print("\nAucuns messages recus")
            else:
                print("\n" + subjects + str(length) + ".Quitter")
                wantedMessageNo = input("Entrez le numero du message que vous voulez ouvrir: ")
                if str(length) == wantedMessageNo:
                    send_msg(self.s, "noConsult")
                    self.__showMainMenu()
                else:
                    send_msg(self.s, "consulting")
                    send_msg(self.s, wantedMessageNo)
                    confirmation = recv_msg(self.s)
                    if confirmation == "messageOk":
                        subject = recv_msg(self.s)
                        subject, extension = subject.split(".")
                        message = recv_msg(self.s)
                        print("\nSujet: " + subject)
                        print(message)
                    elif confirmation == "noMessage":
                        print("Entrez un numero de sujet valide")
                        self.__showMails()
                    else:
                        print("Erreur niveau serveur")
        except Exception as ex:
            print(ex)

    def __showStats(self):
        send_msg(self.s, str(5))
        send_msg(self.s, self.username)

        try:
            nbrMessage = recv_msg(self.s)
            size = recv_msg(self.s)
            messageList = recv_msg(self.s)
            print("\nNombre de message: " + nbrMessage)
            print("Taille du dossier: " + size)
            print("Liste de messages:\n" + messageList)

        except Exception as ex:
            print("Erreur niveau serveur")


newClient = Client()