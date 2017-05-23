import pygame, sys
from pygame.locals import *
import random

# Spielgeschwindigkeit
FPS = 40
INCREASESPEED = 6

# Fenster breite und hoehe
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720

# Schlaegergroesse
PADDLESIZE = WINDOWHEIGHT / 2
PADDLEOFFSET = - 40
LINETHICKNESS = 4

# Farben vor definieren
WHITE = [255, 255, 255]
RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]

STARTSPEED = 1
PADDLEUPPERPOSITION = 4
PADDLELOWERPOSITION = WINDOWHEIGHT/4 * 3 - 4


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
        return -1
    elif ballDirX > 0 and paddle2.left+LINETHICKNESS*4 <= ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
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
        postion = WINDOWWIDTH - 150 
    else:
        postion = 150 

    resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (postion, 25)
    SCREEN.blit(resultSurf, resultRect)
    
    

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
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2

    # Ball Flugrichtung
    ballDirX = -STARTSPEED # -1 = links 1 = rechts
    ballDirY = -STARTSPEED # -1 = hoch 1 = runter

    # Startposition der Schlaeger
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2

    # Erstellen der Schlaeger
    paddle1 = pygame.Rect(PADDLEOFFSET,playerOnePosition, LINETHICKNESS*3,PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET , playerTwoPosition, LINETHICKNESS*3,PADDLESIZE)
    ball = pygame.draw.circle(SCREEN, WHITE, (int(ballX),int(ballY)), LINETHICKNESS*4)
    
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ballX,ballY)

    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


                
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
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

if __name__=='__main__':
    main()
