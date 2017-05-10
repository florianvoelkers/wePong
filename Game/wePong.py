import pygame, sys
from pygame.locals import *

# zum ausführen in python "exec(open("C:/Users/Niko/Documents/wePong/Game/wePong.py").read())"  eingeben

# Globale Variablen
# FPS = Spielgeschwindigkeit
FPS = 200
# Fenster breite und höhe
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080

# Schlägergröße
PADDLESIZE = WINDOWHEIGHT / 2
PADDLEOFFSET = 20
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

# Schläger zeichnen
def drawPaddle(paddle):
    #Hält den Schläger auf aus dem Screen zu verschwinden
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS

    pygame.draw.rect(SCREEN, WHITE, paddle)

# Ball zeichnen
def drawBall(ballX,ballY):
    pygame.draw.circle(SCREEN, WHITE, (int(ballX),int(ballY)), LINETHICKNESS*4)

# Ball bewegen
def moveBall(ball,ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

# Überprüfen ob der Ball mit dem oberen oder unteren Rand kollidiert, wenn ja dann wird die Ball richtung verändert
def checkEdgeCollision(ball, ballDirY):
    if ball.top <= (LINETHICKNESS*4) or ball.bottom >= (WINDOWHEIGHT+LINETHICKNESS*4):
        ballDirY = ballDirY * -1
    return ballDirY

# Überprüft ob der Ball mit einem Schläger kollidiertm wenn ja dann wird die Richtung  der Flugbahn verändert
def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX < 0  and paddle1.right+LINETHICKNESS*2 == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX > 0 and paddle2.left+LINETHICKNESS*4 == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else: return 1



def main():
    pygame.init()

    global SCREEN
    # Display Objekt erstellen auf dem dann alles dargestellt wird
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), pygame.FULLSCREEN)    
    pygame.display.set_caption('wePong')

    FPSCLOCK = pygame.time.Clock()

    # Spielfläche in einer Farbe
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

    # Startposition der Schläger
    playerOnePosition = (WINDOWHEIGHT - PADDLESIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE) /2

    # Erstellen der Schläger
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

        # Steuerung linker Schläger
        if pressed[pygame.K_w]:
            paddle1.y = PADDLEUPPERPOSITION
        if pressed[pygame.K_s]:
            paddle1.y = PADDLELOWERPOSITION

        #Steuerung rechter Schläger
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


        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()