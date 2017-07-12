#!/usr/lib/python2.7

import pygame, sys
from pygame.locals import *
import random
import socket
import threading
import os
import Menu


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

GAMESTART = False
GAMEEND = False

LEFTBATPOSITION = 300, WINDOWHEIGHT/2 -35
RIGHTBATPOSITION =WINDOWWIDTH-300 - 70, WINDOWHEIGHT/2 -35


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
    
    leftGoal = pygame.draw.rect(SCREEN, BLUE, (0, WINDOWHEIGHT/2-119, LINETHICKNESS,238))
    leftGoalOutline = pygame.draw.ellipse(SCREEN, RED, (-90, WINDOWHEIGHT/2-120, 200,240))
    leftGoalInnerOutline = pygame.draw.ellipse(SCREEN, BLUE, (-100, WINDOWHEIGHT/2-110, 200,220))
    
    rightGoal = pygame.draw.rect(SCREEN, BLUE, (WINDOWWIDTH-LINETHICKNESS, WINDOWHEIGHT/2-119, LINETHICKNESS,238))
    rightGoalOutline = pygame.draw.ellipse(SCREEN, RED, (WINDOWWIDTH-110, WINDOWHEIGHT/2-120, 200,240))
    rightGoalInnerOutline = pygame.draw.ellipse(SCREEN, BLUE, (WINDOWWIDTH-100, WINDOWHEIGHT/2-110, 200,220))
    
    if init:
        return lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal

def checkEdgeCollision(puck, puckDirY, puckDirX,lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal, score1, score2):

    def resetPuck ():
        puckDiameter = puck.height / 2
        puck.x = int(WINDOWWIDTH/2) - puckDiameter
        puck.y = int(WINDOWHEIGHT/2)-puckDiameter
        puckDirY = random.sample([-1, 1],k=1)[0] * MAXSPEED/2
        puckDirX = random.sample([-1, 1],k=1)[0] * MAXSPEED/2
        return (puck, puckDirY, puckDirX)
    
    #print ("upperedge",puck.colliderect(upperEdge))
    #print ("loweredge",puck.colliderect(lowerEdge) )
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
    newDirY=0
    newDirX=0
    
    if puckDirY >= 0:
        newDirY = puckDirY - DECREASESPEED
    elif puckDirY <= 0:
        newDirY = puckDirY + DECREASESPEED
    if puckDirX >= 0:
        newDirX = puckDirX - DECREASESPEED
    elif puckDirX <= 0:
        newDirX = puckDirX + DECREASESPEED
    return puck ,newDirX, newDirY

def drawBat(player1):
    if player1:
        bat = SCREEN.blit(BATIMAGE, LEFTBATPOSITION)
    else:
        bat = SCREEN.blit(BATIMAGE, RIGHTBATPOSITION)
    return bat

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
    SCREEN.blit(resultSurf, resultRect)
    while True: 
        seconds=(pygame.time.get_ticks()-start_ticks)/300 
        if seconds>6:
            Menu.main()
            pygame.quit()
            sys.exit()
        if seconds >2:
            GAMEEND = True

# Anzeige des Spieler Scores
def displayScore(player, score):
    if score > 10:
        endResult(player)
    if player: 
        postion = 50 
    else:
        postion = WINDOWWIDTH - 250 

    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (postion, 25)
    SCREEN.blit(resultSurf, resultRect)

# Ueberprueft ob ein Punkt erziehlt wurde und gibt den neuen Score zurueck 
def checkPointScored(player,puck, score, puckDirX,puckDirY):

    def resetPuck (score):
        puckDiameter = puck.height / 2
        puck.x = int(WINDOWWIDTH/2) - puckDiameter
        puck.y = int(WINDOWHEIGHT/2)-puckDiameter
        puckDirY = random.sample([-1, 1],k=1)[0] * MAXSPEED/2
        puckDirX = random.sample([-1, 1],k=1)[0] * MAXSPEED/2
        return (puck, puckDirY, puckDirX)

    if player:
        # Ueberprueft ob Player 1 einen Punkt gemacht hat und setzt den Puck wieder in die Mitte
        if puck.right >= WINDOWWIDTH + 30: 
            score += 1
            puck, puckDirX, puckDirY =  resetPuck(score)
            return score, puck, puckDirX, puckDirY
        # Wenn nichts passiert ist
        else: return (score, puck, puckDirX, puckDirY)
    else:
        # UeberprUeft ob Player 2 einen Punkt gemacht hat und setzt den Puck wieder in die Mitte
        if puck.left <= -30: 
            score += 1
            puck, puckDirX, puckDirY =  resetPuck(score)
            return score, puck, puckDirX, puckDirY
        # Wenn nichts passiert ist
        else: return (score, puck, puckDirX, puckDirY)

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

        resultRect.topleft = (WINDOWWIDTH/2 - 25, WINDOWHEIGHT/2-50)


# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,playerSide):
    playerConnection = connection
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global LEFTBATPOSITION
    global RIGHTBATPOSITION
    global GAMEEND

    if playerSide:
        RIGHTPLAYERCONNECTED = True
    else:
        LEFTPLAYERCONNECTED = True

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
        if GAMEEND:
            playerConnection.send("end")



def serverThread():
    # Socket das auf die Verbindung der beiden Spieler wartet und dann Threads
    # fuer die jeweiligen Spieler startet
    global GAMESTART
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED

    gameSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = ""
    port = 5000
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

def main(connection1,connection2):
    pygame.init()

    global SCREEN
    global PUCKIMAGE
    global BATIMAGE
    global BATMASK

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 30
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    global  WINNERFONT, WINNERFONTSIZE
    WINNERFONTSIZE = 100
    WINNERFONT = pygame.font.Font('freesansbold.ttf', WINNERFONTSIZE)

    score1 = 0
    score2 = 0

    # automatischer pfad auf dem Pi funktioniert unter windows nicht
    PUCKIMAGE = pygame.image.load(os.path.join("/home/pi/Desktop/Game/Sprites","puck.png"))
    BATIMAGE = pygame.image.load(os.path.join("/home/pi/Desktop/Game/Sprites","SchlaegerRot.png"))

    #PUCKIMAGE = pygame.image.load(os.path.join("C:/Users/Niko/Documents/wePong/Game/Sprites","puck.png"))
    #BATIMAGE = pygame.image.load(os.path.join("C:/Users/Niko/Documents/wePong/Game/Sprites","SchlaegerRot.png"))
    puckDiameter = PUCKIMAGE.get_height() / 2
    puck = SCREEN.blit(PUCKIMAGE, (int(WINDOWWIDTH/2) - puckDiameter, int(WINDOWHEIGHT/2)-puckDiameter))
    bat1 = drawBat(True)
    bat2 = drawBat(False)

    # Zufaellige Startrichtung des Pucks
    ramdomDir = random.sample([-1, 1],k=2)
    puckDirX = ramdomDir[0] * MAXSPEED/2  # -1 = links 1 = rechts
    puckDirY = ramdomDir[1] * MAXSPEED/2  # -1 = hoch 1 = runter

    # get arena values
    lowerEdge, upperEdge, leftEdge, rightEdge, leftGoal, rightGoal = drawArena(True)

    threading.Thread(target=playerThread, args=(connection1,True)).start()
    threading.Thread(target=playerThread, args=(connection2,False)).start()

    #threading.Thread(target=serverThread, args=()).start()
    threading.Thread(target=countdown, args=()).start()

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

        if GAMESTART:

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

if __name__=='__main__':
    main()
