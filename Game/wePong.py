import pygame, sys
from pygame.locals import *

# zum ausführen in python "exec(open("C:/Users/Niko/Documents/wePong/Game/wePong.py").read())"  eingeben

# Globale Variablen
# FPS = Spielgeschwindigkeit
FPS = 60
# Fenster breite und höhe
WINDOWWIDTH = 1920
WINDOWHEIGHT = 1080

def main():
    pygame.init()

    # Farben vor definieren
    white = [255, 255, 255]
    red = [255, 0, 0]
    blue = [0,0,255]
    green = [0,255,0]

    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT), pygame.FULLSCREEN) 
    pygame.display.set_caption('wePong')

    # Spielfläche in einer Farbe
    screen.fill(blue)
    # Netz in der Mitte
    net = pygame.draw.rect(screen,green,(WINDOWWIDTH/2-4,0,8,WINDOWHEIGHT))
    # Rand oben und unten
    upperEdge = pygame.draw.rect(screen,green,(0,WINDOWHEIGHT-4,WINDOWWIDTH,4))
    lowerEdge = pygame.draw.rect(screen,green,(0,0,WINDOWWIDTH,4))


    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()