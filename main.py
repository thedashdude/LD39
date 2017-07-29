import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

"""LEVEL = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,1,1,1,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,0,0,0,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,1,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,1,1,0]
    ]"""


SCREENRECT = Rect(0, 0, 640, 480)

class Solids():
    def __init__(self):
        self.rects = []
    def add(self,rect):
        self.rects.append(rect)
        return self.rects.index(rect)
    def remove(self,ind):
        del self.rects[ind]
    def collides(self,rect):
        for r in self.rects:
            if r.colliderect(rect):
                return (True, r)
        return (False, None)
    def draw(self,screen):
        for rect in self.rects:
            pygame.draw.rect(screen, (100,100,100), rect)



class Player(pygame.sprite.Sprite):
    speed = 2
    speed_y = 0
    max_speed_y = 31
    speed_jump = -5
    g = 0.1
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = Rect(x,y,32,32)
    def move(self, direction, solids):
        self.rect.move_ip(direction*self.speed, 0)
        hit, rct = solids.collides(self.rect)
        if hit:
            if direction > 0:
                lft = rct.left
                rgt = self.rect.right
                self.rect.right = lft
                #self.rect.left = self.rect.left + lft - rgt
            else:
                rgt = rct.right
                lft = self.rect.left
                self.rect.left = rgt
                #self.rect.right = self.rect.right + rgt - lft
        if self.rect.bottom >= SCREENRECT.bottom:
            self.speed_y = 0
        if abs(self.speed_y) > self.max_speed_y:
            self.speed_y = max(-self.max_speed_y, min(self.speed_y, self.max_speed_y))
        self.rect = self.rect.clamp(SCREENRECT)
        self.rect.move_ip(0,self.speed_y)
        self.speed_y = self.speed_y + self.g
        hit, rct = solids.collides(self.rect)
        if hit:
            if self.speed_y > 0:
                self.speed_y = 0
                top = rct.top
                bot = self.rect.bottom
                self.rect.bottom = top
                #self.rect.top = self.rect.top + top - bot
            else:
                self.speed_y = 0
                bot = rct.bottom
                top = self.rect.top
                self.rect.top = bot
                #self.rect.bottom = self.rect.bottom + bot - top
        hit, rct = solids.collides(self.rect.move(0,1))
        if hit:
            self.speed_y = 0
    def jump(self,solids):
        hit, rct = solids.collides(self.rect.move(0,1))
        if hit and self.speed_y == 0:
            self.speed_y = self.speed_jump





def main(winstyle = 0):
    # Initialize pygame
    pygame.init()
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    player = Player(0,0)
    solids = Solids()
    solids.add( Rect(0,416,640,32) )
    solids.add( Rect(3*32,416-2*32,64,32) )
    solids.add( Rect(5*32,416-1*32,32,32) )
    solids.add( Rect(7*32,416-2*32,32,32*2) )
    clock = pygame.time.Clock()
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()
        #handle player input
        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction,solids)
        if keystate[K_UP]:
            player.jump(solids)


        
        pygame.draw.rect(screen, (0,0,0), SCREENRECT)
        solids.draw(screen)
        pygame.draw.rect(screen, (200,200,0), player.rect)
        pygame.display.flip()
        print(player.speed_y)
        #cap the framerate
        clock.tick(120)
    pygame.time.wait(1000)
    pygame.quit()






if __name__ == '__main__': main()






