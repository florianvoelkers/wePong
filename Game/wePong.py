#!/usr/lib/python2.7

import pygame, sys
from pygame.locals import *
import random
import socket
import threading


# Spielgeschwindigkeit
FPS = 80
INCREASESPEED = 6

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
def checkEdgeCollision(ball, ballDirY):
    if ball.top <= (LINETHICKNESS*4) or ball.bottom >= (WINDOWHEIGHT+LINETHICKNESS*4):
        ballDirY = ballDirY * -1
    return ballDirY

# Ueberprueft ob der Ball mit einem Schlaeger kollidiert wenn ja dann wird die Richtung  der Flugbahn veraendert
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX < 0  and paddle1.right+LINETHICKNESS*2 >= ball.left and paddle1.top <= ball.top and paddle1.bottom >= ball.bottom:
        return -1
    elif ballDirX > 0 and paddle2.left+LINETHICKNESS*2 <= ball.right and paddle2.top <= ball.top and paddle2.bottom >= ball.bottom:
        return -1
    else: return 1

# Ueberprueft ob ein Punkt erziehlt wurde und gibt den neuen Score zurueck 
def checkPointScored(player,ball, score, ballDirX,ballDirY):

    def resetBall (score):
        ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2 + LINETHICKNESS*4
        ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2 - LINETHICKNESS*2
        ballDirY = random.sample([-STARTSPEED, STARTSPEED],k=1)
        ballDirX = random.sample([-STARTSPEED, STARTSPEED],k=1)
        return (ball,ballDirX[0],ballDirY[0])

    if player:
        # Ueberprueft ob Player 1 einen Punkt gemacht hat und setzt den Ball wieder in die Mitte
        if ball.right >= WINDOWWIDTH - PADDLEOFFSET + LINETHICKNESS*5: 
            score += 1
            ball,ballDirX,ballDirY =  resetBall(score)
            return score,ball,ballDirX,ballDirY
        # Wenn nichts passiert ist
        else: return (score,ball,ballDirX,ballDirY)
    else:
        # UeberprUeft ob Player 2 einen Punkt gemacht hat und setzt den Ball wieder in die Mitte
        if ball.left <= PADDLEOFFSET - LINETHICKNESS*5: 
            score += 1
            ball,ballDirX,ballDirY =  resetBall(score)
            return score,ball,ballDirX,ballDirY
        # Wenn nichts passiert ist
        else: return (score,ball,ballDirX,ballDirY)

# Anzeige des Spieler Scores
def displayScore(player, score):
    if player: 
        postion = 150 
    else:
        postion = WINDOWWIDTH - 150 

    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (postion, 25)
    SCREEN.blit(resultSurf, resultRect)



# Thread um die gesendeten Daten der Spielers auszuwerten
def playerThread(connection):
    playerConnection = connection
    global RIGHTPADDLESPEED
    global LEFTPADDLESPEED
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED

    data = playerConnection.recv(1024)
    player = data
    print ("player",player)
    if player == "player1":
        LEFTPLAYERCONNECTED = True
    elif player == "player2":
        RIGHTPLAYERCONNECTED = True

    while True:
        data = playerConnection.recv(1024)
        if data.count(":") == 1:
            name, speed = data.split (":")
            newSpeed = int(speed) * 2
            print (player, newSpeed)
            if player == "player1":
                LEFTPADDLESPEED = int(newSpeed)

            elif player == "player2":
                RIGHTPADDLESPEED = int(newSpeed)

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

def main():
    pygame.init()

    global SCREEN
    global RIGHTPADDLESPEED
    global LEFTPADDLESPEED

    # Einstellungen der Schriftart
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

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

    print ("vor dem  startet des Threads")
    # ServerThread starten
    threading.Thread(target=serverThread, args=()).start()
    print ("nach dem starten des Threads")

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

            drawArena()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball.x,ball.y)

            ball = moveBall(ball, ballDirX, ballDirY)
            ballDirY = checkEdgeCollision(ball, ballDirY)
            ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
            score1,ball,ballDirX,ballDirY = checkPointScored(True, ball, score1, ballDirX,ballDirY)
            score2,ball,ballDirX,ballDirY = checkPointScored(False, ball, score2, ballDirX,ballDirY)


            displayScore(True,score1)
            displayScore(False,score2)


            pygame.display.update()
            FPSCLOCK.tick(FPS)
        else:
            drawArena()
            drawPaddle(paddle1)
            drawPaddle(paddle2)
            drawBall(ball.x,ball.y)
            pygame.display.update()
            FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
