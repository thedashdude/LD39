#import basic pygame modules
import pygame
from pygame.locals import *

class Entity():
    def __init__(self, x=0, y=0, width = 32, height = 32, texture_loc = "textures/test.jpg"):
        self.rect = Rect(x,y,width,height)

        self.new_entities = list()

        self.texture = pygame.image.load(texture_loc)

    def update(self, keystate, mouse_position, mouse_press, collided_entites):
        pass

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


    def update(self, keystate, mouse_position, mouse_press, collided_entites):
        pass
    # def draw(self, screen):
    #   pygame.draw.rect(screen, (200,200,200), self.rect)



class Player(Entity):
    def __init__(self, x=0, y=0):
        super().__init__(x,y)

    def update(self, keystate, mouse_position, mouse_press, collided_entites):
        if keystate[K_UP]:
            self.rect.top = self.rect.top - 2

        if keystate[K_DOWN]:
            self.rect.top = self.rect.top  + 2

        if keystate[K_LEFT]:
            self.rect.left = self.rect.left - 2

        if keystate[K_RIGHT]:
            self.rect.left = self.rect.left  + 2

        for entity in collided_entites:
            print("collided")
            self.prevent_intersection(entity)
        print("loop")