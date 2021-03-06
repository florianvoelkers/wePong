#!/usr/lib/python2.7

import pygame, sys
from pygame.locals import *
import socket
import threading
import os
import WePong
import AirHockey
import Tron
import time



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
MENUSTART = False
PLAYER1CONNECTION = 0
PLAYER1CONNECTION = 0

# Diese Methode setzt die menuRunning Variable auf False wodurch die Funktionen in der Menu Schleife nicht mehr aufgerufen werden
def pauseMenu():
    global menuRunning
    menuRunning = False

# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,firstConnection,playernumber):
    global PLAYER1CONNECTION
    global PLAYER2CONNECTION 
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global MENUSTART

    # In dieser Abfrage werden die neuen Verbindungen zu den Spielern entsprechenden globalen Variablen zugewiesen
    player = ""
    if firstConnection:
        data = connection.recv(1024)
        player = data
        print ("player",player)
        if player == "player1":
            PLAYER1CONNECTION = connection
            LEFTPLAYERCONNECTED = True
        elif player == "player2":
            PLAYER2CONNECTION = connection
            RIGHTPLAYERCONNECTED = True
    else:
        if playernumber == 1:
            PLAYER1CONNECTION = connection
            player = "player1"
        else:
            PLAYER2CONNECTION = connection
            player = "player2"
    
    # Schleife in der die Eingegebenen Daten der Spieler ausgewertet werden
    # Spieler 1 kann ein Spiel aussuchen
    # Bei Spieler 2 wird die Schleife beendet weil er keine Berechtigung hat ein Spiel auszuwaehlen
    while True:
        data = connection.recv(1024)
        if data.count(":") == 1:
            name, game = data.split (":")
            print(player,name,game)
            if player == "player1" and MENUSTART:
                if game == "tron":
                    print ("starte Tron")
                    threading.Thread(target=Tron.main, args=(PLAYER1CONNECTION,PLAYER2CONNECTION,resumeMenu)).start()
                    pauseMenu()
                elif game == "air":
                    threading.Thread(target=AirHockey.main, args=(PLAYER1CONNECTION,PLAYER2CONNECTION,resumeMenu)).start()
                    pauseMenu()
                    return
                elif game == "pong":
                    print("Starte wepong", game,name,player)  
                    threading.Thread(target=WePong.main, args=(PLAYER1CONNECTION,PLAYER2CONNECTION,resumeMenu)).start()
                    pauseMenu()
                    return
            elif player == "player2":
                break
    return

def serverThread():
    # Socket das auf die Verbindung der beiden Spieler wartet und dann Threads
    # fuer die jeweiligen Spieler startet
    global MENUSTART
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED

    gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port=5000
    gameSocket.bind((host,port))
    gameSocket.listen(5)
    playerCount = 0
    while playerCount < 2:
        print ("waiting for", 2-playerCount ,"connection(s)")
        connection,address = gameSocket.accept()
        print ("got connection",address)
        playerCount+= 1
        threading.Thread(target=playerThread, args=(connection,True,0)).start()
    while True:
        if LEFTPLAYERCONNECTED and RIGHTPLAYERCONNECTED:
            MENUSTART = True
            break
    return


# Diese Methode wird mit den Verbindungen zu den Spielern aufgerufen und started dann fuer die jeweiligen Spieler einen playerThread
def resumeMenu(connection1,connection2):
    global menuRunning
    menuRunning = True
    threading.Thread(target=playerThread, args=(connection1,False,1)).start()
    threading.Thread(target=playerThread, args=(connection2,False,2)).start()

def main():
    pygame.init()

    global MENUSCREEN
    global menuRunning
    menuRunning = True

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    MENUSCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption("Menu")

    FPSCLOCK = pygame.time.Clock()

    # Spielflaeche in einer Farbe
    MENUSCREEN.fill(BLACK)

    # ServerThread starten
    threading.Thread(target=serverThread, args=()).start()

    # Das Hintergrundbild einlesen und auf die Bildschirmgroeße anpassen
    backgroundImage = pygame.image.load(os.path.join("/home/pi/Desktop/Game/Sprites","backGround.png"))
    resizedImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
    background = MENUSCREEN.blit(resizedImage, (0 , 0))

    while True:
        time.sleep(0.1)
        while menuRunning:      
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            # Auslesen von Tastatur eingaben
            pressed = pygame.key.get_pressed()
            # Spiel beenden wenn Escape gedrueckt wird
            if pressed[pygame.K_ESCAPE]:
                print ("escape")
                pygame.quit()
                sys.exit()
                return
            # Hier wird das Hintergrundbild dargestellt
            MENUSCREEN.blit(resizedImage, (0 , 0))
            pygame.display.update()
            FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
