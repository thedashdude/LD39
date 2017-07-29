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
        self.speed_x = 0.0
        self.speed_y = 0.0

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
    def to_rads(self,theta):
        return theta/180.0 * np.pi
    def update(self, keystate, mouse_position, mouse_press, entities):
        pass
    def move(self,entities,Type):
        # entities: list of entities
        # Type: the type to check collisions 

        

        self.rect.move_ip(self.speed_x, 0)
        boxes = []
        ents = []
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Type:
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
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Type:
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


    def update(self, keystate, mouse_position, mouse_press, entities):
        pass
    # def draw(self, screen):
    #   pygame.draw.rect(screen, (200,200,200), self.rect)



class Player(Entity):
    def __init__(self, x=0, y=0,w=32,h=32):
        super().__init__(x,y,w,h, texture_loc= "./textures/Player")
        self.speed = 1
        self.energy = 5000
        self.clicked = False

    def update(self, keystate, mouse_position, mouse_press, entities):
        self.speed_x = ( (keystate[K_RIGHT] or keystate[K_d]) - (keystate[K_LEFT]  or keystate[K_a])) * self.speed
        self.speed_y = ( (keystate[K_DOWN] or keystate[K_s]) - (keystate[K_UP] or keystate[K_w]) ) * self.speed
        self.energy -= np.abs(self.speed_x)
        self.energy -= np.abs(self.speed_y)

        self.move(entities,Wall)

        if mouse_press[0] and not self.clicked:
            hold = np.array([mouse_position[0]-self.rect.centerx,mouse_position[1]-self.rect.centery])
            #hold.scale_to_length(1000)
            hold += [self.rect.centerx,self.rect.centery]
            self.new_entities.append(Bullet(self.rect.centerx-2,self.rect.centery-2, [hold[0],hold[1]] ))
            self.clicked = True
        elif not mouse_press[0]:
            self.clicked = False

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
        self.orientation = None

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

class Bullet(Entity):
    def __init__(self, x,y,goal_position):
        super().__init__(x,y,4,4)
        self.speed = 8.0

        self.actual_fucking_location = [x,y]

        self.iters = 1
        self.goal_position = goal_position
        self.direction = pygame.math.Vector2(10,0).angle_to( pygame.math.Vector2(self.goal_position[0]-self.rect.centerx,self.goal_position[1]-self.rect.centery) )

        self.timer = 100
        self.go_to_goal = True
    def update(self,keystate,mouse_position,mouse_press, entities):
        if self.go_to_goal:
            #self.direction = pygame.math.Vector2(10.0,0.0).angle_to( pygame.math.Vector2(self.goal_position[0]-self.rect.centerx,self.goal_position[1]-self.rect.centery) )
            
            self.speed_x = np.cos( self.to_rads( self.direction ) ) * self.speed
            self.speed_y = np.sin( self.to_rads( self.direction ) ) * self.speed
            
            DISTANCE = 100
            if (self.rect.centerx - self.goal_position[0])**2 + (self.rect.centery - self.goal_position[1])**2 < DISTANCE **2 :
                self.goal_position[0] = (self.goal_position[0]-self.rect.centerx)*100 + self.rect.centerx
                self.goal_position[1] = (self.goal_position[1]-self.rect.centery)*100 + self.rect.centery
        self.move(entities,Wall)

        self.timer -= 1
        if self.timer <= 0:
            del entities[entities.index(self)]
    def move(self,entities,Type):
        # entities: list of entities
        # Type: the type to check collisions 
        # This is the default move but it ricochets and also keeps float values of coords


        

        self.rect.move_ip(self.speed_x, 0)
        self.actual_fucking_location[0] += self.speed_x
        boxes = []
        ents = []
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Type:
                boxes.append(k.rect)
                ents.append(k)

        

        rcti = self.rect.collidelist(boxes)
        if rcti != -1:
            rct = boxes[rcti]
            if self.speed_x > 0:
                self.speed_x *= -1
                self.go_to_goal = False
                lft = rct.left
                self.rect.right = lft
                self.actual_fucking_location[0] = self.rect.x
            else:
                self.speed_x *= -1
                self.go_to_goal = False
                rgt = rct.right
                self.rect.left = rgt
                self.actual_fucking_location[0] = self.rect.x
        
        self.rect.move_ip(0, self.speed_y)
        self.actual_fucking_location[1] += self.speed_y
        boxes = []
        ents = []
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Type:
                boxes.append(k.rect)
                ents.append(k)

        rcti = self.rect.collidelist(boxes)
        if rcti != -1:
            rct = boxes[rcti]
            if self.speed_y > 0:
                self.speed_y *= -1
                self.go_to_goal = False
                top = rct.top
                self.rect.bottom = top
                self.actual_fucking_location[1] = self.rect.y
            else:
                self.speed_y *= -1
                self.go_to_goal = False
                bot = rct.bottom
                self.rect.top = bot
                self.actual_fucking_location[1] = self.rect.y
        self.rect.x = int(self.actual_fucking_location[0])
        self.rect.y = int(self.actual_fucking_location[1])
