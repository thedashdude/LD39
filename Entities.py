import numpy as np
import pygame
from pygame.locals import *

from itertools import cycle
import os

from main import FRAME_RATE

DEAFAULT_TEXTURE = pygame.image.load("textures/test.jpg")

class Entity():
    def __init__(self, x=0, y=0, width = 32, height = 32, texture_loc = None, fps = 15):
        self.fps = fps
        self.rect = Rect(x,y,width,height)
        self.speed_x = 0
        self.speed_y = 0

        self.frame_count = cycle(range(FRAME_RATE * self.fps))

        self.new_entities = list()


        self.texture_cycle = None
        self.current_texture = None

        if texture_loc == None:
            self.texture_cycle = cycle([DEAFAULT_TEXTURE])
        else:
            self.load_textures(texture_loc)

        self.current_texture = next(self.texture_cycle)

    def load_textures(self, path):
        textures = list()
        for entry in os.scandir(path):
            if entry.is_file():
                textures.append(pygame.image.load(entry.path))
        self.texture_cycle = cycle(textures)

    def scale_texture(self, texture):
        return texture


    def get_next_texture(self):
        if next(self.frame_count) % self.fps == 0:
            self.current_texture = next(self.texture_cycle)
        return self.current_texture

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
        scaled_texture = self.scale_texture(self.get_next_texture())
        scaled_texture = pygame.transform.smoothscale(scaled_texture, (self.rect.width, self.rect.height))
        screen.blit(scaled_texture, self.rect)

class Test(Entity):
    def __init__(self,x=0,y=0,):
        super().__init__(x,y)


    def update(self, keystate, mouse_position, mouse_press, entites):
        pass
    # def draw(self, screen):
    #   pygame.draw.rect(screen, (200,200,200), self.rect)



class Player(Entity):
    def __init__(self, x=0, y=0,w=32,h=32):
        super().__init__(x,y,w,h, texture_loc= "./textures/Player")
        self.speed = 2
        self.energy = 5000

    def update(self, keystate, mouse_position, mouse_press, entites):
        self.speed_x = (keystate[K_RIGHT] - keystate[K_LEFT]) * self.speed
        self.speed_y = (keystate[K_DOWN] - keystate[K_UP]) * self.speed
        self.energy -= np.abs(self.speed_x)
        self.energy -= np.abs(self.speed_y)
        self.move(entites)

    def scale_texture(self, texture):
        return pygame.transform.scale2x(texture)
    

    def draw(self, screen):

        scaled_texture = pygame.transform.scale2x(self.get_next_texture())
        screen.blit(scaled_texture, self.rect)
        pygame.draw.rect(screen, (20,200,20), Rect(self.rect.left,self.rect.top-4,self.energy/100,4))


class Wall_Manager():
    def __init__(self):
        self.walls = list()

    def addWall(self, wall):
        self.orientWall(wall)
        self.walls.append(wall)

    def orientWall(self, wall):
        pass

wall_manager = Wall_Manager()        

class Wall(Entity):
    def __init__(self, x=0, y=0,w=32,h=32):
        super().__init__(x,y,w,h)
        wall.orientation = None

    def update(self, keystate, mouse_position, mouse_press, entites):
        pass

class TextBox():
    def __init__(self, dia):
        self.dialogue = dia
        self.was_pressed = False

    def update(self, mouse_press):
        if mouse_press[0] and not self.was_pressed:
            self.dialogue = self.dialogue[50:]
            self.was_pressed = True
        elif not mouse_press[0]:
            self.was_pressed = False


    def draw(self, screen):
        myfont = pygame.font.SysFont("Arial", 25)
        label = myfont.render(self.dialogue[:50], 1, (255,255,0))
        screen.blit(label, (20, 350))        

