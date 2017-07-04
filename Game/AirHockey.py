#!/usr/lib/python2.7

import pygame, sys
from pygame.locals import *
import random
import socket
import threading
import os
#import Menu


# Spielgeschwindigkeit
FPS = 60

# Fenster breite und hoehe
WINDOWWIDTH = 1824
WINDOWHEIGHT = 984

LINETHICKNESS = 20

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [198,61,61]
BLUE = [52, 190, 196]
GREEN = [0, 255, 0]

MAXSPEED = 20
DECREASESPEED = 0.06


# Arena zeichnen
def drawArena(init):
    SCREEN.fill(BLUE)
    
    # Rand oben und unten
    net = pygame.draw.rect(SCREEN,RED,(WINDOWWIDTH/2-4, 0, 8, WINDOWHEIGHT))
    centerOuterCircle = pygame.draw.circle(SCREEN, RED, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 100, 0)
    centerFillCircle = pygame.draw.circle(SCREEN, BLUE, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 90, 0)
    centerInnerCircle = pygame.draw.circle(SCREEN, RED, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 20, 0)
    lowerEdge = pygame.draw.rect(SCREEN, RED, (0, WINDOWHEIGHT-LINETHICKNESS, WINDOWWIDTH, LINETHICKNESS))
    upperEdge = pygame.draw.rect(SCREEN, RED, (0, 0, WINDOWWIDTH, LINETHICKNESS))
    leftEdge = pygame.draw.rect(SCREEN, RED, (0, 0, LINETHICKNESS,WINDOWWIDTH))
    rightEdge = pygame.draw.rect(SCREEN, RED, (WINDOWWIDTH-LINETHICKNESS, 0, LINETHICKNESS,WINDOWWIDTH))

    leftGoalOutline = pygame.draw.ellipse(SCREEN, RED, (-90, WINDOWHEIGHT/2-120, 200,240))
    leftGoalInnerOutline = pygame.draw.ellipse(SCREEN, BLUE, (-100, WINDOWHEIGHT/2-110, 200,220))
    leftGoal = pygame.draw.rect(SCREEN, WHITE, (0, WINDOWHEIGHT/2-109, LINETHICKNESS,218))

    rightGoalOutline = pygame.draw.ellipse(SCREEN, RED, (WINDOWWIDTH-110, WINDOWHEIGHT/2-120, 200,240))
    rightGoalInnerOutline = pygame.draw.ellipse(SCREEN, BLUE, (WINDOWWIDTH-100, WINDOWHEIGHT/2-110, 200,220))
    rightGoal = pygame.draw.rect(SCREEN, WHITE, (WINDOWWIDTH-LINETHICKNESS, WINDOWHEIGHT/2-109, LINETHICKNESS,218))
    if init:
        return lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal

def checkEdgeCollision(puck, puckDirY, puckDirX,lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal):
    #print ("upperedge",puck.colliderect(upperEdge))
    #print ("loweredge",puck.colliderect(lowerEdge) )
    if puckDirY < 0  and puck.colliderect(upperEdge) and upperEdge.colliderect(puck):
        puckDirY = puckDirY * -1
    elif puckDirY > 0  and puck.colliderect(lowerEdge) and lowerEdge.colliderect(puck): #and puck.centery > lowerEdge.top:
        puckDirY = puckDirY * -1

    if puckDirX > 0  and puck.colliderect(rightEdge) and rightEdge.colliderect(puck): #and puck.centerx > rightEdge.left:
        puckDirX = puckDirX * -1
    elif puckDirX < 0  and puck.colliderect(leftEdge) and leftEdge.colliderect(puck):
        puckDirX = puckDirX * -1

    return puckDirY,puckDirX

def checkBatCollision(puck, puckDirY, puckDirX, bat):
    if puck.colliderect(bat) and bat.colliderect(puck):
        if puck.centerx < bat.centerx and puck.centery < bat.centery: # puck ist links oben vom schlaeger
            distanceX = bat.centerx - puck.centerx
            distanceY = bat.centery - puck.centery
            distanceSum = distanceX + distanceY
            puckDirY = - MAXSPEED * (distanceY/distanceSum)
            puckDirX = - MAXSPEED * (distanceX/distanceSum)

        elif puck.centerx > bat.centerx and puck.centery < bat.centery: # puck ist rechts oben vom schlaeger
            distanceX = puck.centerx - bat.centerx 
            distanceY = bat.centery - puck.centery
            distanceSum = distanceX + distanceY
            puckDirY = - MAXSPEED * (distanceY/distanceSum)
            puckDirX = MAXSPEED * (distanceX/distanceSum)

        elif puck.centerx < bat.centerx and puck.centery > bat.centery: # puck ist links unten vom schlaeger
            distanceX = bat.centerx - puck.centerx
            distanceY = puck.centery -bat.centery
            distanceSum = distanceX + distanceY
            puckDirY = MAXSPEED * (distanceY/distanceSum)
            puckDirX = - MAXSPEED * (distanceX/distanceSum)

        elif puck.centerx > bat.centerx and puck.centery > bat.centery: # puck ist rechts unten vom schlaeger
            distanceX = puck.centerx - bat.centerx
            distanceY = puck.centery - bat.centery
            distanceSum = distanceX + distanceY
            puckDirY = MAXSPEED * (distanceY/distanceSum)
            puckDirX = MAXSPEED * (distanceX/distanceSum)

    return puckDirY, puckDirX

def drawPuck(puck):
    newPuck = SCREEN.blit(PUCKIMAGE, (puck.x,puck.y))
    return newPuck

def movePuck(puck, puckDirX, puckDirY):
    puck.x += puckDirX
    puck.y += puckDirY
    print(puckDirX,puckDirY)
    if puckDirY > 0:
        newDirY = puckDirY - DECREASESPEED
    elif puckDirY < 0:
        newDirY = puckDirY + DECREASESPEED
    if puckDirX > 0:
        newDirX = puckDirX - DECREASESPEED
    elif puckDirX < 0:
        newDirX = puckDirX + DECREASESPEED
    return puck ,newDirX, newDirY

def drawBat(batX,batY):
    batDiameter = BATIMAGE.get_height() / 2
    bat = SCREEN.blit(BATIMAGE, (batX-batDiameter,batY-batDiameter))
    return bat

def main():
    pygame.init()

    global SCREEN
    global PUCKIMAGE
    global BATIMAGE
    global BATMASK

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    # automatischer pfad auf dem Pi funktioniert unter windows nicht
    #PUCKIMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),"puck.png"))
    #BATIMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),"SchlaegerRot.png"))

    PUCKIMAGE = pygame.image.load(os.path.join("C:/Users/Niko/Documents/wePong/Game/Sprites","puck.png"))
    BATIMAGE = pygame.image.load(os.path.join("C:/Users/Niko/Documents/wePong/Game/Sprites","SchlaegerRot.png"))
    puckDiameter = PUCKIMAGE.get_height() / 2
    puck = SCREEN.blit(PUCKIMAGE, (int(WINDOWWIDTH/2) - puckDiameter, int(WINDOWHEIGHT/2)-puckDiameter))
    bat1 = drawBat(100, WINDOWHEIGHT/2)
    bat2 = drawBat(WINDOWWIDTH-100, WINDOWHEIGHT/2)

    # Zufaellige Startrichtung des Pucks
    ramdomDir = random.sample([-1, 1],k=2)
    puckDirX = ramdomDir[0] * MAXSPEED/2  # -1 = links 1 = rechts
    puckDirY = ramdomDir[1] * MAXSPEED/2  # -1 = hoch 1 = runter

    # get arena values
    lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal = drawArena(True)
    while True:

        # Auslesen von Tastatur eingaben
        pressed = pygame.key.get_pressed()
        # Spiel beenden wenn Escape gedrueckt wird
        if pressed[pygame.K_ESCAPE]:
            print ("escape")
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        drawArena(False)
        drawPuck(puck)
        bat1 = drawBat(500, WINDOWHEIGHT/2)
        bat2 = drawBat(WINDOWWIDTH-500, WINDOWHEIGHT/2)


        puck, puckDirX, puckDirY = movePuck(puck, puckDirX, puckDirY)
        puckDirY, puckDirX = checkEdgeCollision(puck, puckDirY, puckDirX,lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal)
        puckDirY, puckDirX = checkBatCollision(puck, puckDirY, puckDirX, bat1)
        puckDirY, puckDirX = checkBatCollision(puck, puckDirY, puckDirX, bat2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
