#!/usr/lib/python2.7
from __future__ import division
import pygame, sys
from pygame.locals import *
import random
import socket
import threading
import os
import Menu
import time



# Spielgeschwindigkeit
FPS = 60

# Fenster breite und hoehe
WINDOWWIDTH = 1824
WINDOWHEIGHT = 984

LINETHICKNESS = 20

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [198,61,61]
LIGHTBLUE = [52, 190, 196]
DARKBLUE = [48,98,99]
GREEN = [0, 255, 0]
PINK = [252,0,143]
ORANGE = [255,136,0]

GAMESTART = False
GAMEEND = False


def exitMethod():
    global running
    running = False
    #pygame.quit()
    #sys.exit()


def endResult(player):
    global GAMEEND
    global GAMESTART
    
    GAMESTART = False
    start_ticks=pygame.time.get_ticks()
    if player:
        resultSurf = WINNERFONT.render("Player 1 Won!", True, WHITE)
    else:
        resultSurf = WINNERFONT.render("Player 2 Won!", True, WHITE)

    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    AIRSCREEN.blit(resultSurf, resultRect)
    while True: 
        seconds=(pygame.time.get_ticks()-start_ticks)/300 
        if seconds>6:
            break
        if seconds >4:
            GAMEEND = True
    exitMethod()
    return

def checkCollision()
    #print ("if player 2 crash")
    #endResult(true)
    #print ("if player 1 crash")
    #endResult(false)

def countdown():
    global GAMESTART
    start_ticks=pygame.time.get_ticks()

    while GAMESTART == False: 
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 
        drawArena(False)
        if seconds>3:
            GAMESTART = True
        elif seconds > 2:
            resultSurf = WINNERFONT.render("1", True, WHITE)
            resultRect = resultSurf.get_rect()
        elif seconds > 1:
            resultSurf = WINNERFONT.render("2", True, WHITE)
            resultRect = resultSurf.get_rect()
        else: 
            resultSurf = WINNERFONT.render("3", True, WHITE)
            resultRect = resultSurf.get_rect()
        if not GAMESTART:
            resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            AIRSCREEN.blit(resultSurf,resultRect)
            pygame.display.update()
    return

# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,playerSide):
    playerConnection = connection
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global GAMEEND
    global LEFTPLAYERCONNECTION
    global RIGHTPLAYERCONNECTION
    
    if playerSide:
        RIGHTPLAYERCONNECTED = True
        RIGHTPLAYERCONNECTION = playerConnection
    else:
        LEFTPLAYERCONNECTED = True
        LEFTPLAYERCONNECTION = playerConnection

    while True:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            x,y = data.split (":")
            if x != "game":

                if playerSide:
                    print ("player 1 eingabe uebernemen")
                else:
                    print("player 2 eingeaber ueabernehmen")
        if GAMEEND:
            print ("send end")
            playerConnection.send("end\n")
            playerConnection.send("theEnd")
            print ("end sended")
            break
    return


def main(connection1,connection2,callMenu):
    pygame.init()

    global AIRSCREEN
    global running
    running = True

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    TRONSCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 50
    BASICFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), BASICFONTSIZE)
    global  WINNERFONT, WINNERFONTSIZE
    WINNERFONTSIZE = 100
    WINNERFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), WINNERFONTSIZE)

    threading.Thread(target=playerThread, args=(connection1,True)).start()
    threading.Thread(target=playerThread, args=(connection2,False)).start()

    countdown()

    while running:
        
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

        if GAMESTART:

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    callMenu(LEFTPLAYERCONNECTION,RIGHTPLAYERCONNECTION)
    return

if __name__=='__main__':
    main()
