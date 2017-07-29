import random, os.path
import pygame
import world
import Entities
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)
FRAME_RATE = 120

pygame.init()

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
    lst.append(Entities.Test())
    lst.append(Entities.Player(60.0,60.0,16,16))
    lst.append(Entities.Test(100,100))
    lst.append(Entities.Test(200,100))
    lst.append(Entities.Test(200,400))
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