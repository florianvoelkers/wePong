#!/usr/lib/python2.7

import pygame, sys
from pygame.locals import *
import random
import socket
import threading
import subprocess
import os
import inspect
import WePong
import AirHockey


# Spielgeschwindigkeit
FPS = 60

# Fenster breite und hoehe
WINDOWWIDTH = 1824
WINDOWHEIGHT = 984

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
BLACK = [0,0,0]

LEFTPLAYERCONNECTED = False
RIGHTPLAYERCONNECTED = False
GAMESTART = False
PLAYER1CONNECTION = 0
PLAYER1CONNECTION = 0


# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection):
    global PLAYER1CONNECTION
    global PLAYER2CONNECTION 
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global GAMESTART

    data = connection.recv(1024)
    player = data
    print ("player",player)
    if player == "player1":
        PLAYER1CONNECTION = connection
        LEFTPLAYERCONNECTED = True
    elif player == "player2":
        PLAYER2CONNECTION = connection
        RIGHTPLAYERCONNECTED = True

    while True:
        data = connection.recv(1024)
        if data.count(":") == 1:
            name, game = data.split (":")
            
            if player == "player1" and GAMESTART:
                if game == "tron":
                    print ("starte Tron")
                elif game == "air":
                    AirHockey.main(PLAYER1CONNECTION,PLAYER2CONNECTION)
                    print("Starte airhockey")
                    pygame.quit()
                    sys.exit()
                elif game == "pong":
                    WePong.main(PLAYER1CONNECTION,PLAYER2CONNECTION)
                    print("Starte wepong")
                    pygame.quit()
                    sys.exit()

def serverThread():
    # Socket das auf die Verbindung der beiden Spieler wartet und dann Threads
    # fuer die jeweiligen Spieler startet
    global GAMESTART
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    print("ServerThread startet")

    gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port=5000
    gameSocket.bind((host,port))
    gameSocket.listen(5)
    print("socket hoert zu")
    playerCount = 0
    while playerCount < 2:
        print ("waiting for", 2-playerCount ,"connection(s)")
        connection,address = gameSocket.accept()
        print ("got connection",address)
        playerCount+= 1
        threading.Thread(target=playerThread, args=(connection,)).start()
    while True:
        if LEFTPLAYERCONNECTED and RIGHTPLAYERCONNECTED:
            GAMESTART = True
            break

def main():
    pygame.init()

    global SCREEN

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption("Menu")

    FPSCLOCK = pygame.time.Clock()

    # Spielflaeche in einer Farbe
    SCREEN.fill(BLACK)

    # ServerThread starten
    threading.Thread(target=serverThread, args=()).start()

    backgroundImage = pygame.image.load(os.path.join("/home/pi/Desktop/Game/Sprites","backGround.png"))
    resizedImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
    background = SCREEN.blit(resizedImage, (0 , 0))

    while True:

        # Auslesen von Tastatur eingaben
        pressed = pygame.key.get_pressed()
        # Spiel beenden wenn Escape gedrueckt wird
        if pressed[pygame.K_ESCAPE]:
            print ("escape")
            pygame.quit()
            sys.exit()
            return
        if pressed[pygame.K_SPACE]:
            wePong.main()
            #pygame.quit()
       	for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        else:
        	
        	pygame.display.update()
        	FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
