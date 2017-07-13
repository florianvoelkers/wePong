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


def exitMethod():
    global tronRunning
    tronRunning = False
    #pygame.quit()
    #sys.exit()


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
    while True: 
        seconds=(pygame.time.get_ticks()-start_ticks)/300 
        if seconds>6:
            break
        if seconds >4:
            TRONEND = True
    exitMethod()
    return

def checkCollision(playerside,player,tail):
    for x in range(1, len(tail)):
        if player.colliderect(tail[x]):
            endResult(playerside)
            print("collision")

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
    endResult(True)
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
    
    if playerSide:
        RIGHTPLAYERCONNECTED = True
        RIGHTPLAYERCONNECTION = playerConnection
    else:
        LEFTPLAYERCONNECTED = True
        LEFTPLAYERCONNECTION = playerConnection

    while True:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            name:direction = data.split (":")
            if name != "game":
                if playerSide:
                    RIGHTPLAYERDIRECTION = direction
                else:
                    LEFTPLAYERDIRECTION = direction
        if TRONEND:
            print ("send end")
            playerConnection.send("end\n")
            print ("end sended")
            break
    return

def setupPlayer(playerSide):
    if playerSide:
        # linker player (1)
        player = pygame.Rect(50,WINDOWHEIGHT / 2, LINETHICKNESS*3,LINETHICKNESS*5)
    else:
        # rechter player(2)
        player = pygame.Rect(WINDOWWIDTH - 100,WINDOWHEIGHT / 2, LINETHICKNESS*3,LINETHICKNESS*5)
    return player

def movePlayer(player,xDir,yDir):
        player.x + xDir
        player.y + yDir
    return player

def applyDirection(playerSide,xDir,yDir):
    global LEFTPLAYERDIRECTION
    global RIGHTPLAYERDIRECTION

    newXDir,newYDir = xDir,newYDir
    if playerSide:
        direction = LEFTPLAYERDIRECTION
        LEFTPLAYERDIRECTION = "none"
    else:
        direction = RIGHTPLAYERDIRECTION
        RIGHTPLAYERDIRECTION = "none"

    if direction == "right" and xDir == -1:
        newXDir,newYDir = 0,-1
    elif direction == "right" and xDir == 1:
        newXDir,newYDir = 0,1
    elif direction == "right" and yDir == -1:
        newXDir,newYDir = 1,0
    elif direction == "right" and yDir == 1:
        newXDir,newYDir -1,0
    
    if direction == "left" and xDir == -1:
        newXDir,newYDir = 0,1
    elif direction == "left" and xDir == 1:
        newXDir,newYDir = 0,-1
    elif direction == "left" and yDir == -1:
        newXDir,newYDir = -1,0
    elif direction == "left" and yDir == 1:
        newXDir,newYDir = 1,0

    return newXDir, newYDir

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
        pygame.draw.rect(PONGSCREEN, ORANGE, player)
    else:
        pygame.draw.rect(PONGSCREEN, PINK, player)
    return pygame.Rect(player.x,player.y,player.width,player.height)

def main(connection1,connection2,callMenu):
    pygame.init()

    global TRONSCREEN
    global tronRunning
    tronRunning = True

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

    player1 = setupPlayer(True)
    player2 = setupPlayer(False)
    p1DirX = 1
    p1DirY = 0
    p2DirX = -1
    p2DirY = 0

    player1Tail = []
    player2Tail = []

    TRONSCREEN.fill(DARKBLUE)
    for x in range (0,15):
        pygame.draw.rect(TRONSCREEN, LIGHTBLUE, (0, x*61, WINDOWWIDTH, LINETHICKNESS))
    for x in range(0,20):
        pygame.draw.rect(TRONSCREEN, LIGHTBLUE, (x*91, 0, LINETHICKNESS,WINDOWWIDTH))

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
            player1Tail[len(player1Tail)+1] = drawPlayer(player1, True)
            player2Tail[len(player2Tail)+1] = drawPlayer(player2, False)
            checkCollision(player1, player2Tail)
            checkCollision(player2, player1Tail)
            p1DirX, p1DirY = applyDirection(True,p1DirX,p1DirY):
            p2DirX, p2DirY = applyDirection(False, p2DirX, p2DirY):
            player1 = movePlayer(player1, p1DirX, p1DirY)
            player2 =movePlayer(player2, p2DirX, p2DirY)
            
            print("TRONSTART")

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    callMenu(LEFTPLAYERCONNECTION,RIGHTPLAYERCONNECTION)
    return

if __name__=='__main__':
    main()
