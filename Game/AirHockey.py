#!/usr/lib/python2.7
from __future__ import division
import pygame, sys
from pygame.locals import *
import random
import socket
import threading
import os
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
BLUE = [52, 190, 196]
GREEN = [0, 255, 0]

MAXSPEED = 20
DECREASESPEED = 0.04

AIRSTART = False
AIREND = False

# Positionen der Schlaeger festlegen
LEFTBATPOSITION = 500, WINDOWHEIGHT/2 -35
RIGHTBATPOSITION = WINDOWWIDTH-500 - 70, WINDOWHEIGHT/2 -35

# Diese Methode setzt die Variable airRunning auf False dadurch wird die Game Schleife beendet und das Spiel angehalten
def exitMethod():
    global airRunning
    airRunning = False

# Arena zeichnen
# Durch das uebereinander legen von Kreisen und langen Rechtecken war es moeglich das Spielfeld zu erstellen
# Wenn init = True ist dann werden die Raender und Tore zurueck gegeben
def drawArena(init):
    AIRSCREEN.fill(BLUE)
    
    net = pygame.draw.rect(AIRSCREEN,RED,(WINDOWWIDTH/2-4, 0, 8, WINDOWHEIGHT))
    centerOuterCircle = pygame.draw.circle(AIRSCREEN, RED, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 100, 0)
    centerFillCircle = pygame.draw.circle(AIRSCREEN, BLUE, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 90, 0)
    centerInnerCircle = pygame.draw.circle(AIRSCREEN, RED, (int(WINDOWWIDTH/2),int(WINDOWHEIGHT/2)), 20, 0)
    lowerEdge = pygame.draw.rect(AIRSCREEN, RED, (0, WINDOWHEIGHT-LINETHICKNESS, WINDOWWIDTH, LINETHICKNESS))
    upperEdge = pygame.draw.rect(AIRSCREEN, RED, (0, 0, WINDOWWIDTH, LINETHICKNESS))
    leftEdge = pygame.draw.rect(AIRSCREEN, RED, (0, 0, LINETHICKNESS,WINDOWWIDTH))
    rightEdge = pygame.draw.rect(AIRSCREEN, RED, (WINDOWWIDTH-LINETHICKNESS, 0, LINETHICKNESS,WINDOWWIDTH))
    
    leftGoal = pygame.draw.rect(AIRSCREEN, BLUE, (0, WINDOWHEIGHT/2-119, LINETHICKNESS,238))
    leftGoalOutline = pygame.draw.ellipse(AIRSCREEN, RED, (-90, WINDOWHEIGHT/2-120, 200,240))
    leftGoalInnerOutline = pygame.draw.ellipse(AIRSCREEN, BLUE, (-100, WINDOWHEIGHT/2-110, 200,220))
    
    rightGoal = pygame.draw.rect(AIRSCREEN, BLUE, (WINDOWWIDTH-LINETHICKNESS, WINDOWHEIGHT/2-119, LINETHICKNESS,238))
    rightGoalOutline = pygame.draw.ellipse(AIRSCREEN, RED, (WINDOWWIDTH-110, WINDOWHEIGHT/2-120, 200,240))
    rightGoalInnerOutline = pygame.draw.ellipse(AIRSCREEN, BLUE, (WINDOWWIDTH-100, WINDOWHEIGHT/2-110, 200,220))
    
    if init:
        return lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal

# Mit dieser Methode wird uberprueft ob der Puck an einem Randstueck abprallen muss, ist das der Fall wird die Flugrichtung angepasst
# Bei einer Kollision mit einem Tor wird der Score erhoet und der puck mit einer zufaelligen Flugrichtung in der Mitte des Spielfeldes platziert
def checkEdgeCollision(puck, puckDirY, puckDirX,lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal, score1, score2):

    def resetPuck ():
        puckDiameter = puck.height / 2
        puck.x = int(WINDOWWIDTH/2) - puckDiameter
        puck.y = int(WINDOWHEIGHT/2)-puckDiameter
        puckDirY = random.sample([-1, 1],k=1)[0] * MAXSPEED/2
        puckDirX = random.sample([-1, 1],k=1)[0] * MAXSPEED/2
        return (puck, puckDirY, puckDirX)
    
    if puckDirY < 0  and puck.colliderect(upperEdge) and upperEdge.colliderect(puck):
        puckDirY = puckDirY * -1
    elif puckDirY > 0  and puck.colliderect(lowerEdge) and lowerEdge.colliderect(puck):
        puckDirY = puckDirY * -1

    if puckDirX > 0 and puck.colliderect(rightGoal) and puck.top > rightGoal.top and puck.bottom < rightGoal.bottom:
        score1 += 1
        puck, puckDirX, puckDirY =  resetPuck()
        return score1, score2, puck, puckDirX, puckDirY
    elif puckDirX > 0  and puck.colliderect(rightEdge) and rightEdge.colliderect(puck):
        puckDirX = puckDirX * -1
    elif puckDirX < 0 and puck.colliderect(leftGoal) and puck.top > leftGoal.top and puck.bottom < leftGoal.bottom:
        score2 += 1
        puck, puckDirX, puckDirY =  resetPuck()
        return score1, score2, puck, puckDirX, puckDirY
    elif puckDirX < 0  and puck.colliderect(leftEdge) and leftEdge.colliderect(puck):
        puckDirX = puckDirX * -1

    return score1, score2, puck, puckDirY, puckDirX

# Diese Methode ueberprueft Kollisionen zwischen dem mitgegbenen Schlager und dem Puck
# Bei einer Kollision wird die neue Flugrichtung des Pucks berechnet und zurueck gegeben
def checkBatCollision(puck, puckDirY, puckDirX, bat):
    global MAXSPEED
    newDirY,newDirX = 0,0
    if puck.colliderect(bat) and bat.colliderect(puck):

        if puck.centerx < bat.centerx and puck.centery < bat.centery: # puck ist links oben vom schlaeger
            distanceX = bat.centerx - puck.centerx
            distanceY = bat.centery - puck.centery
            distanceSum = distanceX + distanceY
            newDirY = - MAXSPEED * (distanceY/distanceSum)
            newDirX = - MAXSPEED * (distanceX/distanceSum)

        elif puck.centerx > bat.centerx and puck.centery < bat.centery: # puck ist rechts oben vom schlaeger
            distanceX = puck.centerx - bat.centerx 
            distanceY = bat.centery - puck.centery
            distanceSum = distanceX + distanceY
            newDirY = - MAXSPEED * (distanceY/distanceSum)
            newDirX = MAXSPEED * (distanceX/distanceSum)

        elif puck.centerx < bat.centerx and puck.centery > bat.centery: # puck ist links unten vom schlaeger
            distanceX = bat.centerx - puck.centerx
            distanceY = puck.centery -bat.centery
            distanceSum = distanceX + distanceY
            newDirY = MAXSPEED * (distanceY/distanceSum)
            newDirX = - MAXSPEED * (distanceX/distanceSum)

        elif puck.centerx > bat.centerx and puck.centery > bat.centery: # puck ist rechts unten vom schlaeger
            distanceX = puck.centerx - bat.centerx
            distanceY = puck.centery - bat.centery
            distanceSum = distanceX + distanceY
            newDirY = MAXSPEED * (distanceY/distanceSum)
            newDirX = MAXSPEED * (distanceX/distanceSum)
    else:
        newDirY = puckDirY
        newDirX = puckDirX
    return newDirY, newDirX

# Der Puck wird mit dieser Methode gezeichnet
def drawPuck(puck):
    newPuck = AIRSCREEN.blit(PUCKIMAGE, (puck.x,puck.y))
    return newPuck

# Diese Methode wendet die Bewegungsrichtung auf den Puck an und gibt die neue Position zurueck
def movePuck(puck, puckDirX, puckDirY):
    puck.x += puckDirX
    puck.y += puckDirY
    newDirX, newDirY = 0,0
    if puckDirY >= 0:
        newDirY = puckDirY - DECREASESPEED
    elif puckDirY <= 0:
        newDirY = puckDirY + DECREASESPEED
    if puckDirX >= 0:
        newDirX = puckDirX - DECREASESPEED
    elif puckDirX <= 0:
        newDirX = puckDirX + DECREASESPEED

    return puck ,newDirX, newDirY

# Diese Methode zeichnet die Schlaeger des jeweils mitgegebenen Spielers und gibt ihn zurueck
def drawBat(player1):
    if player1:
        bat = AIRSCREEN.blit(BATIMAGE, LEFTBATPOSITION)
    else:
        bat = AIRSCREEN.blit(BATIMAGE, RIGHTBATPOSITION)
    return bat

# Diese Methode bekommt ueber einen boolean Wert gesagt ob Player 1 = True oder 2 = False gewonnen hat
# Der jeweilige Gewinner wird dann in grosser Schrift in der mitte des Bildschirms angezeigt und nach der vorgegebenen Zeit wird die exitMethode aufgerufen
def endResult(player):
    global AIREND
    global AIRSTART
    
    AIRSTART = False
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
            AIREND = True
    exitMethod()
    return

# Anzeige des Spieler Scores an der jeweiligen Stelle fuer die verschiedenen Spieler
def displayScore(player, score):
    if score > 2:
        endResult(player)
    if player: 
        postion = 80 
    else:
        postion = WINDOWWIDTH - 280 

    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (postion, 25)
    AIRSCREEN.blit(resultSurf, resultRect)


# Die countdown Methode zeigt zu Beginn des Spiels einen Countdown auf der Mitte des Spielfeldes an
# Am ende des Countdowns wird AIRSTART auf True gesetzt wodurch das Spiel gestartet wird
# Die Methode drawArena wird auch immer wieder aufgerufen damit der Countdown sich nicht ueberschreibt
def countdown():
    global AIRSTART
    start_ticks=pygame.time.get_ticks()

    while AIRSTART == False: 
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 
        drawArena(False)
        if seconds>3:
            AIRSTART = True
        elif seconds > 2:
            resultSurf = WINNERFONT.render("1", True, WHITE)
            resultRect = resultSurf.get_rect()
        elif seconds > 1:
            resultSurf = WINNERFONT.render("2", True, WHITE)
            resultRect = resultSurf.get_rect()
        else: 
            resultSurf = WINNERFONT.render("3", True, WHITE)
            resultRect = resultSurf.get_rect()
        if not AIRSTART:
            resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
            AIRSCREEN.blit(resultSurf,resultRect)
            pygame.display.update()
    return

# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,playerSide):
    playerConnection = connection
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global LEFTBATPOSITION
    global RIGHTBATPOSITION
    global AIREND
    global LEFTPLAYERCONNECTION
    global RIGHTPLAYERCONNECTION
    
    if playerSide:
        LEFTPLAYERCONNECTED = True
        LEFTPLAYERCONNECTION = playerConnection
    else:
        RIGHTPLAYERCONNECTED = True
        RIGHTPLAYERCONNECTION = playerConnection

    # In dieser Schleife werden die gesendeten Daten der Spieler ausgelesen und in Globalen Variablen gespeichert
    while True:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            x,y = data.split (":")
            if x != "game":
                newX = int(x)
                newY = int(y)
                if playerSide:
                    LEFTBATPOSITION = newX * (WINDOWWIDTH/200),(WINDOWHEIGHT/100) * newY
                else:
                    RIGHTBATPOSITION = newX * (WINDOWWIDTH/200) + WINDOWWIDTH/2  ,(WINDOWHEIGHT/100) * newY

        # Wenn AIREND gesetzt wird bekommen die Player die Nachricht end damit die App wieder in das Hauptmenu geht          	         
        if AIREND:
            playerConnection.send("end\n")
            break
    return

# Dies ist die Main-Methode des Spiels die aus dem Menu aufgerufen wird
# Es werden die Verbindungen zu den Spielern mitgegeben und ein callback um das Menu wieder zu starten
def main(connection1,connection2,callMenu):
    pygame.init()

    global AIRSCREEN
    global PUCKIMAGE
    global BATIMAGE
    global BATMASK
    global airRunning
    airRunning = True

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    AIRSCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 50
    BASICFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), BASICFONTSIZE)
    global  WINNERFONT, WINNERFONTSIZE
    WINNERFONTSIZE = 100
    WINNERFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), WINNERFONTSIZE)

    score1 = 0
    score2 = 0

    PUCKIMAGE = pygame.image.load(os.path.join("/home/pi/Desktop/Game/Sprites","puck.png"))
    BATIMAGE = pygame.image.load(os.path.join("/home/pi/Desktop/Game/Sprites","SchlaegerRot.png"))

    puckDiameter = PUCKIMAGE.get_height() / 2
    puck = AIRSCREEN.blit(PUCKIMAGE, (int(WINDOWWIDTH/2) - puckDiameter, int(WINDOWHEIGHT/2)-puckDiameter))
    bat1 = drawBat(True)
    bat2 = drawBat(False)

    # Zufaellige Startrichtung des Pucks
    ramdomDir = random.sample([-1, 1],k=2)
    puckDirX = ramdomDir[0] * MAXSPEED/2  # -1 = links 1 = rechts
    puckDirY = ramdomDir[1] * MAXSPEED/2  # -1 = hoch 1 = runter

    # Teile der Arena speichern
    lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal = drawArena(True)

    # starten der PlayerThreads
    threading.Thread(target=playerThread, args=(connection1,True)).start()
    threading.Thread(target=playerThread, args=(connection2,False)).start()

    # starten des Countdowns
    countdown()

    # Haupschleife des Spiels
    while airRunning:
        
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

        if AIRSTART:
            drawArena(False)
            drawPuck(puck)
            bat1 = drawBat(True)
            bat2 = drawBat(False)

            puck, puckDirX, puckDirY = movePuck(puck, puckDirX, puckDirY)
            score1, score2, puck, puckDirY, puckDirX = checkEdgeCollision(puck, puckDirY, puckDirX,lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal, score1, score2)
            puckDirY, puckDirX = checkBatCollision(puck, puckDirY, puckDirX, bat1)
            puckDirY, puckDirX = checkBatCollision(puck, puckDirY, puckDirX, bat2)

            displayScore(True,score1)
            displayScore(False,score2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    # Wenn die airRunning - Schleife unterbrochen wird, wird wieder das Menu aufgerufen und die Spielerverbindungen werden zurueck uebergeben
    callMenu(LEFTPLAYERCONNECTION,RIGHTPLAYERCONNECTION)
    return

if __name__=='__main__':
    main()
