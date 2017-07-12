#!/usr/lib/python2.7

import pygame, sys
from pygame.locals import *
import random
import socket
import threading
import Menu


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
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

STARTSPEED = 1
MAXSPEED = 2.4
PADDLESTARTPOSTION = WINDOWHEIGHT / 2 - PADDLESIZE/2
PADDLEUPPERPOSITION = 4
PADDLELOWERPOSITION = (WINDOWHEIGHT/4) * 2 - 44

LEFTPADDLESPEED = 0
RIGHTPADDLESPEED = 0
GAMEEND = False
GAMESTART = False
LEFTPLAYERCONNECTED = False
RIGHTPLAYERCONNECTED = False


# Arena zeichnen
def drawArena():
    SCREEN.fill(BLUE)
    net = pygame.draw.rect(SCREEN,GREEN,(WINDOWWIDTH/2-4, 0, 8, WINDOWHEIGHT))

    # Rand oben und unten
    upperEdge = pygame.draw.rect(SCREEN, GREEN, (0, WINDOWHEIGHT-LINETHICKNESS, WINDOWWIDTH, LINETHICKNESS))
    lowerEdge = pygame.draw.rect(SCREEN, GREEN, (0, 0, WINDOWWIDTH, LINETHICKNESS))
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
    pygame.draw.rect(SCREEN, WHITE, paddle)

# Ball zeichnen
def drawBall(ballX,ballY):
    pygame.draw.circle(SCREEN, WHITE, (int(ballX),int(ballY)), LINETHICKNESS*4)

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
            newXDir, newYDir = 0.5, -1.5
        elif percent > 0.6:
            newXDir, newYDir = 1.5, -0.5
        elif percent > 0.4:
            newXDir, newYDir = -1 * ballDirX, ballDirY
        elif percent > 0.2:
            newXDir, newYDir = 1.5, 0.5
        else:
            newXDir, newYDir = 0.5, 1.5
        return newXDir, newYDir            
    elif ballDirX > 0 and ball.colliderect(paddle2) and paddle2.colliderect(ball):
        contactpoint = paddle2.top - ball.centery
        percent =(contactpoint / PADDLESIZE) +1
        if percent > 0.8:
            newXDir, newYDir = -0.5, -1.5
        elif percent > 0.6:
            newXDir, newYDir = -1.5, -0.5
        elif percent > 0.4:
            newXDir, newYDir = -1 * ballDirX, ballDirY
        elif percent > 0.2:
            newXDir, newYDir = -1.5, 0.5
        else:
            newXDir, newYDir = -0.5, 1.5
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

def endResult(player):
    global GAMEEND
    global GAMESTART
    GAMESTART = False

    start_ticks=pygame.time.get_ticks()
    if player:
        resultSurf = WINNERFONT.render("Player 1 Wins!", True, WHITE)
    else:
        resultSurf = WINNERFONT.render("Player 2 Wins!", True, WHITE)

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

def countdown():
    global GAMESTART
    start_ticks=pygame.time.get_ticks()

    while GAMESTART == False: 
        seconds=(pygame.time.get_ticks()-start_ticks)/1000 
        drawArena()
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
        SCREEN.blit(resultSurf, resultRect)


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



# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection,playerSide):
    playerConnection = connection
    global RIGHTPADDLESPEED
    global LEFTPADDLESPEED
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED
    global GAMEEND

    if playerSide:
        RIGHTPLAYERCONNECTED = True
    else:
        LEFTPLAYERCONNECTED = True

    while True:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            name, speed = data.split (":")
            newSpeed = int(speed) * 2
            if playerSide:
                LEFTPADDLESPEED = int(newSpeed)
            else:
                RIGHTPADDLESPEED = int(newSpeed)
        if GAMEEND:
            playerConnection.send("end")

# Thread der auf neue Verbindungen wartet
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
            print ("gamestart = true und break der whileschleife")
            GAMESTART = True
            break

def main(connection1,connection2):
    pygame.init()

    global SCREEN
    global RIGHTPADDLESPEED
    global LEFTPADDLESPEED

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 30
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    global  WINNERFONT, WINNERFONTSIZE
    WINNERFONTSIZE = 100
    WINNERFONT = pygame.font.Font('freesansbold.ttf', WINNERFONTSIZE)

    # Display Objekt erstellen auf dem dann alles dargestellt wird
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))#, pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    score1 = 0
    score2 = 0


    # Spielflaeche in einer Farbe
    SCREEN.fill(BLUE)
    # Netz in der Mitte
    net = pygame.draw.rect(SCREEN,GREEN,(WINDOWWIDTH/2-4,0,8,WINDOWHEIGHT))
    # Rand oben und unten
    upperEdge = pygame.draw.rect(SCREEN,GREEN,(0,WINDOWHEIGHT-LINETHICKNESS,WINDOWWIDTH,LINETHICKNESS))
    lowerEdge = pygame.draw.rect(SCREEN,GREEN,(0,0,WINDOWWIDTH,LINETHICKNESS))

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

    ball = pygame.draw.circle(SCREEN, WHITE, (int(ballX),int(ballY)), LINETHICKNESS*4)
    
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ballX,ballY)
    
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
                    
            # Steuerung linker Schlaeger mit Tastatur
            if pressed[pygame.K_w]:
                paddle1.y = paddle1.y - 5
            if pressed[pygame.K_s]:
                paddle1.y = paddle1.y + 5

            #Steuerung rechter Schlaeger mit Tastatur
            if pressed[pygame.K_UP]:
                paddle2.y = paddle2.y - 5
            if pressed[pygame.K_DOWN]:
                paddle2.y = paddle2.y + 5

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

if __name__=='__main__':
    main()
