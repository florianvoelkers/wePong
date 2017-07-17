#!/usr/lib/python2.7
from __future__ import division
import pygame, sys
from pygame.locals import *
import socket
import threading
import os
import time



# Spielgeschwindigkeit
FPS = 60

# Fenster breite und hoehe
WINDOWWIDTH = 1824
WINDOWHEIGHT = 984

LINETHICKNESS = 4

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [198,61,61]
LIGHTBLUE = [52, 190, 196]
DARKBLUE = [48,98,99]
GREEN = [0, 255, 0]
PINK = [252,0,143]
ORANGE = [255,136,0]

TRONSTART = False
TRONEND = False

LEFTPLAYERDIRECTION = "none"
RIGHTPLAYERDIRECTION = "none"

MOVESPEED = 3

# Diese Methode setzt die Variable tronRunning auf False dadurch wird die Game Schleife beendet und das Spiel angehalten
def exitMethod():
    global tronRunning
    tronRunning = False

# Diese Methode bekommt ueber einen boolean Wert gesagt ob Player 1 = True oder 2 = False gewonnen hat
# Der jeweilige Gewinner wird dann in grosser Schrift in der mitte des Bildschirms angezeigt und nach der vorgegebenen Zeit wird die exitMethode aufgerufen
def endResult(player):
    global TRONEND
    global TRONSTART
    
    TRONSTART = False
    start_ticks=pygame.time.get_ticks()
    if player:
        resultSurf = WINNERFONT.render("Player 1 Won!", True, WHITE)
    else:
        resultSurf = WINNERFONT.render("Player 2 Won!", True, WHITE)

    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    TRONSCREEN.blit(resultSurf, resultRect)
    pygame.display.update()
    while True: 
        seconds=(pygame.time.get_ticks()-start_ticks)/300 
        if seconds>5:
            break
        if seconds >4:
            TRONEND = True
    exitMethod()
    return

# In dieser Methode wird ueberprueft ob der mitgegebene player mit der uebergebenen Spur(tail) kollidiert ist
# Ueber die playerside wird der daraus resultierende Gewinner mitgegeben, mit dem im fall einer Kollision die endResult Methode aufgerufen wird
def checkCollision(playerside,player,tail):
    for x in range(1, len(tail)):
        if player.colliderect(tail[x]) and x < len(tail)-22:
            endResult(playerside)

# Die countdown Methode zeigt zu Beginn des Spiels einen Countdown auf der Mitte des Spielfeldes an
# Am ende des Countdowns wird TRONSTART auf True gesetzt wodurch das Spiel gestartet wird
# Und der Hintergrund und das Hintergrundgitter werden immer neu gezeichnet damit der Countdown sich nicht ueberschreibt
def countdown():
    global TRONSTART
    start_ticks=pygame.time.get_ticks()

    while TRONSTART == False: 
        seconds=(pygame.time.get_ticks()-start_ticks)/1000
        TRONSCREEN.fill(DARKBLUE)

        for x in range (0,15):
            pygame.draw.rect(TRONSCREEN, LIGHTBLUE, (0, x*61, WINDOWWIDTH, LINETHICKNESS))
        for x in range(0,20):
            pygame.draw.rect(TRONSCREEN, LIGHTBLUE, (x*91, 0, LINETHICKNESS,WINDOWWIDTH))

        if seconds>3:
            TRONSTART = True
        elif seconds > 2:
            resultSurf = WINNERFONT.render("1", True, WHITE)
            resultRect = resultSurf.get_rect()
        elif seconds > 1:
            resultSurf = WINNERFONT.render("2", True, WHITE)
            resultRect = resultSurf.get_rect()
        else: 
            resultSurf = WINNERFONT.render("3", True, WHITE)
            resultRect = resultSurf.get_rect()
        if not TRONSTART:
            resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            TRONSCREEN.blit(resultSurf,resultRect)
            pygame.display.update()
    return

# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,playerSide):
    playerConnection = connection
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global TRONEND
    global LEFTPLAYERCONNECTION
    global RIGHTPLAYERCONNECTION
    global RIGHTPLAYERDIRECTION
    global LEFTPLAYERDIRECTION
    global tronRunning
    
    if playerSide:
        LEFTPLAYERCONNECTED = True
        LEFTPLAYERCONNECTION = playerConnection
    else:
        RIGHTPLAYERCONNECTED = True
        RIGHTPLAYERCONNECTION = playerConnection

    # In dieser Schleife werden die gesendeten Daten der Spieler ausgelesen und in Globalen Variablen gespeichert
    while tronRunning:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            name,direction = data.split (":")
            if name != "game":
                if playerSide:
                    if direction == "left" or direction == "right":
                        LEFTPLAYERDIRECTION = direction
                else:
                    if direction == "left" or direction == "right":
                        RIGHTPLAYERDIRECTION = direction
                        
    # Wenn tronRunning False ist bekommen die Player die Nachricht end damit die App wieder in das Hauptmenu geht          	         
    playerConnection.send("end\n")
    return

# Diese Methode erzeugt die Rechtecke(Fahrzeuge) der Spieler und gibt sie zurueck
def setupPlayer(playerSide):
    if playerSide:
        # linker player (1)
        player = pygame.Rect(50,WINDOWHEIGHT / 2, LINETHICKNESS*5,LINETHICKNESS*5)
    else:
        # rechter player(2)
        player = pygame.Rect(WINDOWWIDTH - 100,WINDOWHEIGHT / 2, LINETHICKNESS*5,LINETHICKNESS*5)
    return player

# Mit dieser Methode wird die aktuelle Bewegung auf das Player objekt uebertrgen
def movePlayer(player,xDir,yDir):
    player.x += xDir
    player.y += yDir
    return player

# Diese Methode bekommt die SpielerSeite uebergeben und die Richtung in die sich der Spieler aktuell bewegt
# Diese wird dann je nach eingabe der Spieler veraendert und zurueck gegeben
def applyDirection(playerSide,xDir,yDir):
    global LEFTPLAYERDIRECTION
    global RIGHTPLAYERDIRECTION

    newXDir,newYDir = xDir,yDir
    if playerSide:
        direction = LEFTPLAYERDIRECTION
        LEFTPLAYERDIRECTION = "none"
    else:
        direction = RIGHTPLAYERDIRECTION
        RIGHTPLAYERDIRECTION = "none"

    if direction == "right" and xDir == -MOVESPEED:
        newXDir,newYDir = 0,-MOVESPEED
    elif direction == "right" and xDir == MOVESPEED:
        newXDir,newYDir = 0,MOVESPEED
    elif direction == "right" and yDir == -MOVESPEED:
        newXDir,newYDir = MOVESPEED,0
    elif direction == "right" and yDir == MOVESPEED:
        newXDir,newYDir=-MOVESPEED,0
        
    if direction == "left" and xDir == -MOVESPEED:
        newXDir,newYDir = 0,MOVESPEED
    elif direction == "left" and xDir == MOVESPEED:
        newXDir,newYDir = 0,-MOVESPEED
    elif direction == "left" and yDir == -MOVESPEED:
        newXDir,newYDir = -MOVESPEED,0
    elif direction == "left" and yDir == MOVESPEED:
        newXDir,newYDir = MOVESPEED,0

    return newXDir, newYDir

# Mit dieser Methode werden die Fahrzeuge der Spieler gezeichnet und es wird ueberprueft
# ob sie gegen den Rand gefahren sind weil das auch zum Game Over fuehrt
def drawPlayer(player,playerSide):
    if player.bottom > WINDOWHEIGHT - LINETHICKNESS:
        if playerSide:
            endResult(False)
        else:
            endResult(True)
    elif player.top < LINETHICKNESS:
        if playerSide:
            endResult(False)
        else:
            endResult(True)
    if playerSide:
        pygame.draw.rect(TRONSCREEN, ORANGE, player)
    else:
        pygame.draw.rect(TRONSCREEN, PINK, player)
    return pygame.Rect(player.x,player.y,player.width,player.height)

# Dies ist die Main-Methode des Spiels die aus dem Menu aufgerufen wird
# Es werden die Verbindungen zu den Spielern mitgegeben und ein callback um das Menu wieder zu starten
def main(connection1,connection2,callMenu):
    pygame.init()

    global TRONSCREEN
    global tronRunning
    tronRunning = True

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    TRONSCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))# ,pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 50
    BASICFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), BASICFONTSIZE)
    global  WINNERFONT, WINNERFONTSIZE
    WINNERFONTSIZE = 100
    WINNERFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), WINNERFONTSIZE)

    # Starten der PlayerThreads mit den uebergebenen Verbindungen
    threading.Thread(target=playerThread, args=(connection1,True)).start()
    threading.Thread(target=playerThread, args=(connection2,False)).start()

    # Initialisierung der Spieler
    player1 = setupPlayer(True)
    player2 = setupPlayer(False)
    p1DirX = MOVESPEED
    p1DirY = 0
    p2DirX = -MOVESPEED
    p2DirY = 0

    # Initialisierung der Arrays in denen die Spuren der Spieler gespeichert werden
    player1Tail = []
    player2Tail = []

    # Zeichnen des Hintergrunds
    TRONSCREEN.fill(DARKBLUE)
    for x in range (0,15):
        pygame.draw.rect(TRONSCREEN, LIGHTBLUE, (0, x*61, WINDOWWIDTH, LINETHICKNESS))
    for x in range(0,20):
        pygame.draw.rect(TRONSCREEN, LIGHTBLUE, (x*91, 0, LINETHICKNESS,WINDOWWIDTH))

    # Starten des Countdowns
    countdown()

    while tronRunning:
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

        if TRONSTART:
        	# Hier werden die Spieler an der neuen position gezeichnet und die neue Stelle wird dem Array angehaengt das die Spur speichert
            player1Tail.append(drawPlayer(player1, True))
            player2Tail.append(drawPlayer(player2, False))

            # Ueberpruefung ob die Spieler mit sich selbst oder dem Gegner kollidiert sind
            checkCollision(True,player1, player2Tail)
            checkCollision(False,player1, player1Tail)
            checkCollision(False,player2, player1Tail)
            checkCollision(True,player2, player2Tail)

            # Abfragen der neuen Richtung
            p1DirX, p1DirY = applyDirection(True,p1DirX,p1DirY)
            p2DirX, p2DirY = applyDirection(False, p2DirX, p2DirY)

            # Anwenden der neuen Bewegungsrichtung
            player1 = movePlayer(player1, p1DirX, p1DirY)
            player2 = movePlayer(player2, p2DirX, p2DirY)
            
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    # Wenn die tronRunningschleife unterbrochen wird wird wieder das Menu aufgerufen und die Spielerverbindungen werden zurueck uebergeben
    callMenu(LEFTPLAYERCONNECTION,RIGHTPLAYERCONNECTION)
    return

if __name__=='__main__':
    main()
