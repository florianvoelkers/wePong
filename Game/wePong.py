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
INCREASESPEED = 5

# Fenster breite und hoehe
WINDOWWIDTH = 1824
WINDOWHEIGHT = 984

# Schlaegergroesse
PADDLESIZE = WINDOWHEIGHT / 8
PADDLEOFFSET = 40
LINETHICKNESS = 4

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [67, 66, 124]
GREEN = [255, 136, 0]

STARTSPEED = 1
MAXSPEED = 2.4
PADDLESTARTPOSTION = WINDOWHEIGHT / 2 - PADDLESIZE/2
PADDLEUPPERPOSITION = 4
PADDLELOWERPOSITION = (WINDOWHEIGHT/4) * 2 - 44

LEFTPADDLESPEED = 0
RIGHTPADDLESPEED = 0
PONGEND = False
PONGSTART = False
LEFTPLAYERCONNECTED = False
RIGHTPLAYERCONNECTED = False

# Diese Methode setzt die Variable pongRunning auf False dadurch wird die Game Schleife beendet und das Spiel angehalten
def exitMethod():
    global pongRunning
    pongRunning = False

# Arena zeichnen
def drawArena():
    PONGSCREEN.fill(BLUE)
    net = pygame.draw.rect(PONGSCREEN,GREEN,(WINDOWWIDTH/2-4, 0, 8, WINDOWHEIGHT))

    # Rand oben und unten
    upperEdge = pygame.draw.rect(PONGSCREEN, GREEN, (0, WINDOWHEIGHT-LINETHICKNESS, WINDOWWIDTH, LINETHICKNESS))
    lowerEdge = pygame.draw.rect(PONGSCREEN, GREEN, (0, 0, WINDOWWIDTH, LINETHICKNESS))
    return lowerEdge, upperEdge

# Schlaeger zeichnen
def drawPaddle(paddle):
    #Stoppt den Schlaeger am unteren Rand
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Stoppt den Schlaeger am oberen Rand
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS
    #Schlaeger zeichnen
    pygame.draw.rect(PONGSCREEN, GREEN, paddle)

# Ball zeichnen
def drawBall(ballX,ballY):
    pygame.draw.circle(PONGSCREEN, WHITE, (int(ballX),int(ballY)), LINETHICKNESS*4)

# Ball bewegen
def moveBall(ball,ballDirX, ballDirY):
    ball.x += (ballDirX * INCREASESPEED)
    ball.y += (ballDirY * INCREASESPEED)
    return ball

# Ueberpruefen ob der Ball mit dem oberen oder unteren Rand kollidiert, wenn ja dann wird die Ball richtung veraendert
def checkEdgeCollision(ball, ballDirY, lowerEdge, upperEdge):
    if ballDirY > 0  and ball.colliderect(upperEdge) and upperEdge.colliderect(ball):
        ballDirY = ballDirY * -1
    elif ballDirY < 0  and ball.colliderect(lowerEdge) and lowerEdge.colliderect(ball):
        ballDirY = ballDirY * -1
    return ballDirY

# Ueberprueft ob der Ball mit einem Schlaeger kollidiert wenn ja dann wird die Richtung  der Flugbahn veraendert
def checkHitBall(ball, paddle1, paddle2, ballDirX, ballDirY):
    #print (ball.center,ball.top,ball.bottom,ball.left,ball.right,ball.x,ball.y)
    if ballDirX < 0  and ball.colliderect(paddle1) and paddle1.colliderect(ball):
        contactpoint = paddle1.top - ball.centery
        percent =(contactpoint / PADDLESIZE) +1
        if percent > 0.8:
            newXDir, newYDir = 1, -3
        elif percent > 0.6:
            newXDir, newYDir = 3, -1
        elif percent > 0.4:
            newXDir, newYDir = -1 * ballDirX, ballDirY
        elif percent > 0.2:
            newXDir, newYDir = 3, 1
        else:
            newXDir, newYDir = 1, 3
        return newXDir, newYDir            
    elif ballDirX > 0 and ball.colliderect(paddle2) and paddle2.colliderect(ball):
        contactpoint = paddle2.top - ball.centery
        percent =(contactpoint / PADDLESIZE) +1
        if percent > 0.8:
            newXDir, newYDir = -1, -3
        elif percent > 0.6:
            newXDir, newYDir = -3, -1
        elif percent > 0.4:
            newXDir, newYDir = -1 * ballDirX, ballDirY
        elif percent > 0.2:
            newXDir, newYDir = -3, 1
        else:
            newXDir, newYDir = -1, 3
        return newXDir, newYDir        
    else: 
        return ballDirX, ballDirY

# Ueberprueft ob ein Punkt erziehlt wurde und gibt den neuen Score zurueck 
def checkPointScored(player,ball, score, ballDirX,ballDirY):

    def resetBall ():
        ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2 + LINETHICKNESS*4
        ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2 - LINETHICKNESS*2
        ballDirY = random.sample([-STARTSPEED, STARTSPEED],k=1)
        ballDirX = random.sample([-STARTSPEED, STARTSPEED],k=1)
        return (ball,ballDirX[0],ballDirY[0])

    if player:
        # Ueberprueft ob Player 1 einen Punkt gemacht hat und setzt den Ball wieder in die Mitte
        if ball.right >= WINDOWWIDTH + LINETHICKNESS*4: 
            score += 1
            ball,ballDirX,ballDirY =  resetBall()
            return score,ball,ballDirX,ballDirY
        # Wenn nichts passiert ist
        else: return (score,ball,ballDirX,ballDirY)
    else:
        # UeberprUeft ob Player 2 einen Punkt gemacht hat und setzt den Ball wieder in die Mitte
        if ball.left <= 0: 
            score += 1
            ball,ballDirX,ballDirY =  resetBall()
            return score,ball,ballDirX,ballDirY
        # Wenn nichts passiert ist
        else: return (score,ball,ballDirX,ballDirY)

# Diese Methode bekommt ueber einen boolean Wert gesagt ob Player 1 = True oder 2 = False gewonnen hat
# Der jeweilige Gewinner wird dann in grosser Schrift in der mitte des Bildschirms angezeigt und nach der vorgegebenen Zeit wird die exitMethode aufgerufen
def endResult(player):
    global PONGEND
    global PONGSTART
    PONGSTART = False

    start_ticks=pygame.time.get_ticks()
    if player:
        resultSurf = WINNERFONT.render("Player 1 Wins!", True, WHITE)
    else:
        resultSurf = WINNERFONT.render("Player 2 Wins!", True, WHITE)

    resultRect = resultSurf.get_rect()
    resultRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
    PONGSCREEN.blit(resultSurf, resultRect)
    pygame.display.update()
    while True: 
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 
        if seconds>5:
            break    	    
        if seconds >4:
            PONGEND = True
    exitMethod()
    return

# Die countdown Methode zeigt zu Beginn des Spiels einen Countdown auf der Mitte des Spielfeldes an
# Am ende des Countdowns wird PONGSTART auf True gesetzt wodurch das Spiel gestartet wird
# Die Methode drawArena wird auch immer wieder aufgerufen damit der Countdown sich nicht ueberschreibt
def countdown():
    global PONGSTART
    start_ticks=pygame.time.get_ticks()

    while PONGSTART == False: 
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 
        drawArena()
        if seconds>3:
            PONGSTART = True
        elif seconds > 2:
            resultSurf = WINNERFONT.render("1", True, WHITE)
            resultRect = resultSurf.get_rect()
        elif seconds > 1:
            resultSurf = WINNERFONT.render("2", True, WHITE)
            resultRect = resultSurf.get_rect()
        else: 
            resultSurf = WINNERFONT.render("3", True, WHITE)
            resultRect = resultSurf.get_rect()
        if not PONGSTART:
            resultRect.topleft = (WINDOWWIDTH/2 - 25, WINDOWHEIGHT/2-50)
            PONGSCREEN.blit(resultSurf, resultRect)
            pygame.display.update()
    return

# Anzeige des Spieler Scores
def displayScore(player, score):
    if score > 4:
        endResult(player)
    if player: 
        postion = 80 
    else:
        postion = WINDOWWIDTH - 280 

    resultSurf = BASICFONT.render('Score = %s' %(score), True, GREEN)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (postion, 25)
    PONGSCREEN.blit(resultSurf, resultRect)



# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,playerSide):
    playerConnection = connection
    global RIGHTPADDLESPEED
    global LEFTPADDLESPEED
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global PONGEND
    global LEFTPLAYERCONNECTION
    global RIGHTPLAYERCONNECTION

    if playerSide:
        LEFTPLAYERCONNECTED = True
        LEFTPLAYERCONNECTION = connection
    else:
        RIGHTPLAYERCONNECTED = True
        RIGHTPLAYERCONNECTION = connection
    
    while True:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            name, speed = data.split (":")
            if speed != "pong":
                newSpeed = int(speed) * 2
                if playerSide:
                    LEFTPADDLESPEED = int(newSpeed)
                else:
                    RIGHTPADDLESPEED = int(newSpeed)
        # Wenn PONGEND gesetzt wird bekommt die App ein "end" gesendet was sie in das Hauptmenu zurueck kehren laesst
        if PONGEND:
            playerConnection.send("end\n")
            break
    return

def main(connection1,connection2,callMenu):
    pygame.init()

    global PONGSCREEN
    global RIGHTPADDLESPEED
    global LEFTPADDLESPEED
    global pongRunning
    global PONGEND
    global menuInstance

    pongRunning = True
    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 50
    BASICFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), BASICFONTSIZE)

    global  WINNERFONT, WINNERFONTSIZE
    WINNERFONTSIZE = 100
    WINNERFONT = pygame.font.Font(os.path.join("/home/pi/Desktop/Game/Font",'ARCADE.TTF'), WINNERFONTSIZE)

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    PONGSCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    score1 = 0
    score2 = 0
    PONGEND = False

    # Spielflaeche in einer Farbe
    PONGSCREEN.fill(BLUE)
    # Netz in der Mitte
    net = pygame.draw.rect(PONGSCREEN,GREEN,(WINDOWWIDTH/2-4,0,8,WINDOWHEIGHT))
    # Rand oben und unten
    upperEdge = pygame.draw.rect(PONGSCREEN,GREEN,(0,WINDOWHEIGHT-LINETHICKNESS,WINDOWWIDTH,LINETHICKNESS))
    lowerEdge = pygame.draw.rect(PONGSCREEN,GREEN,(0,0,WINDOWWIDTH,LINETHICKNESS))

    # Ball Startposition
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2 + LINETHICKNESS*4
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2 - LINETHICKNESS*2

    # Ball Flugrichtung
    ramdomDir = random.sample([-STARTSPEED, STARTSPEED],k=2)
    ballDirX = ramdomDir[0]  # -1 = links 1 = rechts
    ballDirY = ramdomDir[1] # -1 = hoch 1 = runter

    # Startposition der Schlaeger
    playerOnePosition = PADDLESTARTPOSTION
    playerTwoPosition = PADDLESTARTPOSTION

    # Erstellen der Schlaeger
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS*3,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET , playerTwoPosition, LINETHICKNESS*3,PADDLESIZE)

    # Erstellen des Balls
    ball = pygame.draw.circle(PONGSCREEN, WHITE, (int(ballX),int(ballY)), LINETHICKNESS*4)
    
    # Erstes Zeichen der Arena, der Schlaeger und des Balls
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ballX,ballY)
    
    # Starten der Playerthreads
    threading.Thread(target=playerThread, args=(connection1,True)).start()
    threading.Thread(target=playerThread, args=(connection2,False)).start()
    
    # Starten des Countdowns
    countdown()
    
    # Haupschleife des Spiels
    while pongRunning:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # Auslesen von Tastatur eingaben
        pressed = pygame.key.get_pressed()
        # Spiel beenden wenn Escape gedrueckt wird
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            
        if PONGSTART:

            # Steuerung linker Schlaeger mit Handydaten
            paddle1.y = paddle1.y + LEFTPADDLESPEED

            #Steuerung rechter Schlaeger mit Handydaten
            paddle2.y = paddle2.y + RIGHTPADDLESPEED

            lowerEdge, upperEdge = drawArena()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball.x,ball.y)

            ball = moveBall(ball, ballDirX, ballDirY)
            ballDirY = checkEdgeCollision(ball, ballDirY,lowerEdge, upperEdge)
            ballDirX, ballDirY = checkHitBall(ball, paddle1, paddle2, ballDirX, ballDirY)
            score1,ball,ballDirX,ballDirY = checkPointScored(True, ball, score1, ballDirX,ballDirY)
            score2,ball,ballDirX,ballDirY = checkPointScored(False, ball, score2, ballDirX,ballDirY)

            displayScore(True,score1)
            displayScore(False,score2)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    # Wenn pongRunning auf False gesetzt wird beendet sich die Haupschleife und das Menu wird mit den Spielerverbindungen aufgerufen
    callMenu(LEFTPLAYERCONNECTION,RIGHTPLAYERCONNECTION)
    return

if __name__=='__main__':
    main()
