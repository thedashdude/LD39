import random, os.path
import pygame
import world
import Entities
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)
FRAME_RATE = 60

pygame.init()
def level(lst):
    for i in range(0,100):
        lst.append(Entities.Wall(i*16,0))
        lst.append(Entities.Wall(i*16,29*16))
    for i in range(0,100):
        lst.append(Entities.Wall(0,i*16))
        lst.append(Entities.Wall(39*16,i*16))
    for i in range(0,10):
        lst.append(Entities.Wall(6*16,i*16))
    for i in range(0,10):
        lst.append(Entities.Wall(i*16+16*10,16*5))
    for i in range(0,10):
        lst.append(Entities.Wall(i*16+16*10,16*9))
    for i in range(0,10):
        lst.append(Entities.Wall(i*16+16*10,16*14))
    for i in range(0,10):
        lst.append(Entities.Wall(i*16+16*10,16*24))
    for i in range(0,30):
        lst.append(Entities.Wall(24*16,i*16+16*5))

def test_quit():
    for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return True
    return False

def main(winstyle = 0):
    # Initialize pygame
    pygame.init()
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    clock = pygame.time.Clock()
    pygame.display.flip()
    lst = []
    lst.append(Entities.Player(60.0,60.0))
    level(lst)

    #lst.append(Entities.Wall(100,100))
    #lst.append(Entities.Wall(200,100))
    #lst.append(Entities.Wall(200,400))
    lst.append(Entities.Energy(400,400))
    lst.append(Entities.Enemy(300,300))
    lst.append(Entities.Enemy(300,200))
    lst.append(Entities.Enemy(300,100))
    lst.append(Entities.Enemy(300,40))
    lst.append(Entities.Enemy(600,300))
    #lst.append(Entities.Wall(300,300))
    s=""
    for i in range(0, 100):
        s += str(i)
    tb = Entities.TextBox(s)

    wrld = world.World(lst,tb, screen)

    display = pygame.display

    while wrld.cont():
        if test_quit(): return

        keystate = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        pygame.draw.rect(screen, (0,0,0), SCREENRECT)
        

        wrld.update(keystate,mousePos,mousePressed)
        wrld.draw_all()


        pygame.display.flip()
        clock.tick(FRAME_RATE)
        
    pygame.time.wait(1000)
    pygame.quit()

if __name__ == '__main__': main()