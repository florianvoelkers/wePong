import pygame, sys
from pygame.locals import *
import random
import socket
import threading


# Spielgeschwindigkeit
FPS = 40
INCREASESPEED = 6

# Fenster breite und hoehe
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720

# Schlaegergroesse
PADDLESIZE = WINDOWHEIGHT / 2
PADDLEOFFSET = 40
LINETHICKNESS = 4

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

STARTSPEED = 1
PADDLEUPPERPOSITION = 4
PADDLELOWERPOSITION = (WINDOWHEIGHT/4) * 2 - 4

LEFTPADDLEUP = False
LEFTPADDLESPEED = 1
RIGHTPADDLEUP = False
RIGHTPADDLESPEED = 1

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
    if ballDirX < 0  and paddle1.right+LINETHICKNESS*2 >= ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1 * RIGHTPADDLESPEED
    elif ballDirX > 0 and paddle2.left+LINETHICKNESS*4 <= ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1 * LEFTPADDLESPEED
    else: return 1

# Ueberprueft ob ein Punkt erziehlt wurde und gibt den neuen Score zurueck 
def checkPointScored(player,ball, score, ballDirX,ballDirY):

    def resetBall (score):
        ball.x = WINDOWWIDTH/2 - LINETHICKNESS/2
        ball.y = WINDOWHEIGHT/2 - LINETHICKNESS/2
        ballDirY = random.sample([-1, 1],k=1)
        ballDirX = random.sample([-1, 1],k=1)
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
    global RIGHTPADDLEUP
    global RIGHTPADDLESPEED
    global LEFTPLAYERCONNECTED
    global RIGHTPLAYERCONNECTED

    data = playerConnection.recv(1024)
    player = data
    if player == "player1":
        LEFTPLAYERCONNECTED = True
    elif player == "player2":
        RIGHTPLAYERCONNECTED = True

    while True:
        data = playerConnection.recv(1024)
        position, speed = data.split (":")
        print (player,position, speed)

        if player == "player1":
            if position == "up":
                LEFTPADDLEUP = True
            elif position == "down":
                LEFTPADDLEUP = False
            LEFTPADDLESPEED = speed

        elif player == "player2":
            if position == "up":
                RIGHTPADDLEUP = True
            elif position == "down":
                RIGHTPADDLEUP = False
            RIGHTPADDLESPEED = speed


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
    while True:
        print ("in while schleife des servers")
        if LEFTPLAYERCONNECTED and RIGHTPLAYERCONNECTED:
           print ("gamestart = true und break der whileschleife")
           GAMESTART = True
           break
        else:
            connection,address = gameSocket.accept()
            threading.Thread(target=playerThread, args=(connection,)).start()


def main():
    pygame.init()

    global SCREEN

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
    playerOnePosition = PADDLELOWERPOSITION
    playerTwoPosition = PADDLELOWERPOSITION

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

        if GAMESTART:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                    
            # Steuerung linker Schlaeger
            if pressed[pygame.K_w]:
                paddle1.y = PADDLEUPPERPOSITION
            if pressed[pygame.K_s]:
                paddle1.y = PADDLELOWERPOSITION

            #Steuerung rechter Schlaeger
            if pressed[pygame.K_UP]:
                paddle2.y = PADDLEUPPERPOSITION
            if pressed[pygame.K_DOWN]:
                paddle2.y = PADDLELOWERPOSITION


            if LEFTPADDLEUP:
                paddle1.y = PADDLEUPPERPOSITION
            else:
                paddle1.y = PADDLELOWERPOSITION

            #Steuerung rechter Schlaeger
            if RIGHTPADDLEUP:
                paddle2.y = PADDLEUPPERPOSITION
            else:
                paddle2.y = PADDLELOWERPOSITION


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
