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

LINETHICKNESS = 8

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [198,61,61]
BLUE = [52, 190, 196]
GREEN = [0, 255, 0]


# Arena zeichnen
def drawArena():

    
    SCREEN.fill(BLUE)
    
    # Rand oben und unten
    net = pygame.draw.rect(SCREEN,RED,(WINDOWWIDTH/2-4, 0, 8, WINDOWHEIGHT))
    centerOuterCircle = pygame.draw.circle(SCREEN, RED, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 100, 0)
    centerFillCircle = pygame.draw.circle(SCREEN, BLUE, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 90, 0)
    centerInnerCircle = pygame.draw.circle(SCREEN, RED, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 20, 0)
    upperEdge = pygame.draw.rect(SCREEN, RED, (0, WINDOWHEIGHT-LINETHICKNESS, WINDOWWIDTH, LINETHICKNESS))
    lowerEdge = pygame.draw.rect(SCREEN, RED, (0, 0, WINDOWWIDTH, LINETHICKNESS))
    leftEdge = pygame.draw.rect(SCREEN, RED, (0, 0, LINETHICKNESS,WINDOWWIDTH))
    rightEdge = pygame.draw.rect(SCREEN, RED, (WINDOWWIDTH-LINETHICKNESS, 0, LINETHICKNESS,WINDOWWIDTH))

    leftGoalOutline = pygame.draw.ellipse(SCREEN, RED, (-100, WINDOWHEIGHT/2-120, 200,240))
    leftGoalInnerOutline = pygame.draw.ellipse(SCREEN, BLUE, (-110, WINDOWHEIGHT/2-110, 200,220))
    leftGoal = pygame.draw.rect(SCREEN, WHITE, (0, WINDOWHEIGHT/2-110, LINETHICKNESS,220))

    rightGoalOutline = pygame.draw.ellipse(SCREEN, RED, (WINDOWWIDTH-100, WINDOWHEIGHT/2-120, 200,240))
    rightGoalInnerOutline = pygame.draw.ellipse(SCREEN, BLUE, (WINDOWWIDTH-90, WINDOWHEIGHT/2-110, 200,220))
    rightGoal = pygame.draw.rect(SCREEN, WHITE, (WINDOWWIDTH-LINETHICKNESS, WINDOWHEIGHT/2-110, LINETHICKNESS,220))
    return lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal

def drawPuck(puck):
    puckDiameter = PUCKIMAGE.get_height() / 2
    newPuck = SCREEN.blit(PUCKIMAGE, (puck.x-puckDiameter,puck.y-puckDiameter))
    return newPuck

def drawBat(batX,batY):
    batDiameter = BATIMAGE.get_height() / 2
    SCREEN.blit(BATIMAGE, (batX-batDiameter,batY-batDiameter))

def main():
    pygame.init()

    global SCREEN
    global PUCKIMAGE
    global BATIMAGE
    # Display Objekt erstellen auf dem dann alles dargestellt wird
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')
    
    # automatischer pfad auf dem Pi funktioniert unter windows nicht
    #PUCKIMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),"puck.png"))
    #BATIMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.dirname(__file__)),"SchlaegerRot.png"))

    PUCKIMAGE = pygame.image.load(os.path.join("C:/Users/Niko/Documents/wePong/Game/Sprites","puck.png"))
    BATIMAGE = pygame.image.load(os.path.join("C:/Users/Niko/Documents/wePong/Game/Sprites","SchlaegerRot.png"))
    FPSCLOCK = pygame.time.Clock()

    puck = SCREEN.blit(PUCKIMAGE, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)))

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

        lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal = drawArena()
        drawPuck(puck)
        drawBat(100, WINDOWHEIGHT/2)
        drawBat(WINDOWWIDTH-100, WINDOWHEIGHT/2)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
