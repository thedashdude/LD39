import random, os.path
import pygame
import world
from pygame.locals import *

SCREENRECT = Rect(0, 0, 640, 480)

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
    wrld = world.World([],screen)
    display = pygame.display


    while wrld.cont():
        if test_quit(): return
        keystate = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        mousePressed = pygame.mouse.get_pressed()
        

        wrld.update(keystate,mousePos,mousePressed)
        wrld.draw_all()


        pygame.display.flip()
        
    pygame.time.wait(1000)
    pygame.quit()






if __name__ == '__main__': main()