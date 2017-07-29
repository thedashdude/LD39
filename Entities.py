#import basic pygame modules
import numpy as np
import pygame
from pygame.locals import *

class Entity():
    def __init__(self, x=0, y=0, width = 32, height = 32, texture_loc = "textures/test.jpg"):
        self.rect = Rect(x,y,width,height)
        self.speed_x = 0
        self.speed_y = 0

        self.new_entities = list()

        self.texture = pygame.image.load(texture_loc)

    def update(self, keystate, mouse_position, mouse_press, entites):
        pass
    def move(self,entites):
        #collided_entites.append( Rect(-100,-100,10,10) )

        

        self.rect.move_ip(self.speed_x, 0)
        boxes = []
        ents = []
        for k in entites:
            if self.rect.colliderect(k.rect) and k != self:
            	boxes.append(k.rect)
            	ents.append(k)

        

        rcti = self.rect.collidelist(boxes)
        if rcti != -1:
            rct = boxes[rcti]
            if self.speed_x > 0:
                self.speed_x = 0
                lft = rct.left
                self.rect.right = lft
            else:
                self.speed_x = 0
                rgt = rct.right
                self.rect.left = rgt
        
        self.rect.move_ip(0, self.speed_y)
        boxes = []
        ents = []
        for k in entites:
            if self.rect.colliderect(k.rect) and k != self:
            	boxes.append(k.rect)
            	ents.append(k)

        rcti = self.rect.collidelist(boxes)
        if rcti != -1:
            rct = boxes[rcti]
            if self.speed_y > 0:
                self.speed_y = 0
                top = rct.top
                self.rect.bottom = top
            else:
                self.speed_y = 0
                bot = rct.bottom
                self.rect.top = bot

    def prevent_intersection(self, entity):
        pass

    def get_new_entities(self):
        x = self.new_entities
        self.new_entities = list()
        return x

    def draw(self, screen):
        
        scaled_texture = pygame.transform.scale(self.texture, (self.rect.width, self.rect.height))
        screen.blit(scaled_texture, self.rect)

class Test(Entity):
    def __init__(self,x=0,y=0):
        super().__init__(x,y)


    def update(self, keystate, mouse_position, mouse_press, entites):
        pass
    # def draw(self, screen):
    #   pygame.draw.rect(screen, (200,200,200), self.rect)



class Player(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x,y)
        self.speed = 2

    def update(self, keystate, mouse_position, mouse_press, entites):
        self.speed_x = (keystate[K_RIGHT] - keystate[K_LEFT]) * self.speed
        self.speed_y = (keystate[K_DOWN] - keystate[K_UP]) * self.speed
        self.move(entites)