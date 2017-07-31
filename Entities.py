import numpy as np
import pygame
from pygame.locals import *

from itertools import cycle
import os

from main import FRAME_RATE

DEAFAULT_TEXTURE_LOC = "textures/default"

class Entity():
    def __init__(self, x=0, y=0, width = 32, height = 32, texture_loc = DEAFAULT_TEXTURE_LOC, fps = 15, load_texture = True):
        self.fps = fps
        self.update_freq = FRAME_RATE // self.fps

        self.rect = Rect(x,y,width,height)
        self.speed_x = 0.0
        self.speed_y = 0.0

        self.frame_count = cycle(range(self.update_freq))

        self.new_entities = list()

        self.texture_cycle = None
        self.current_texture = None
        self.texture_loc = texture_loc

        if load_texture:
            self.load_textures()

            self.current_texture = next(self.texture_cycle)

    def load_textures(self):
        textures = list()
        for entry in os.scandir(self.texture_loc):
            if entry.is_file():
                texture = pygame.image.load(entry.path)
                scaled_texture = pygame.transform.smoothscale(texture, (self.rect.width, self.rect.height))
                textures.append(scaled_texture)



        self.texture_cycle = cycle(textures)

    def get_next_texture(self):
        current_frame = next(self.frame_count)
        if current_frame == 0:
            self.current_texture = next(self.texture_cycle)
        return self.current_texture

    def scale_texture(self, texture):
        return texture

    def update(self, keystate, mouse_position, mouse_press, entites):
        pass

    def to_rads(self,theta):
        #theta: in degrees, return in radians.
        return theta/180.0 * np.pi

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

    def get_new_entities(self):
        x = self.new_entities
        self.new_entities = list()
        return x

    def draw(self, screen):
        #scaled_texture = pygame.transform.smoothscale(self.get_next_texture(), (self.rect.width, self.rect.height))

        screen.blit(self.get_next_texture(), self.rect)


class Test(Entity):
    def __init__(self,x=0,y=0,):
        super().__init__(x,y)


    def update(self, keystate, mouse_position, mouse_press, entities):
        pass
    # def draw(self, screen):
    #   pygame.draw.rect(screen, (200,200,200), self.rect)



class Player(Entity):
    def __init__(self, x=0, y=0,width=320,height=320):
        super().__init__(x=x, y=y, width=width, height=height, texture_loc= "./textures/Player")
        self.speed = 1
        self.energy = 5000
        self.clicked = False

    def update(self, keystate, mouse_position, mouse_press, entities):
        self.speed_x = ( (keystate[K_RIGHT] or keystate[K_d]) - (keystate[K_LEFT]  or keystate[K_a])) * self.speed
        self.speed_y = ( (keystate[K_DOWN] or keystate[K_s]) - (keystate[K_UP] or keystate[K_w]) ) * self.speed
        self.energy -= np.abs(self.speed_x)
        self.energy -= np.abs(self.speed_y)

        self.move(entities,Wall)

        #shoot if clicked
        if mouse_press[0] and not self.clicked:
            hold = np.array([mouse_position[0]-self.rect.centerx,mouse_position[1]-self.rect.centery])
            #hold.scale_to_length(1000)
            hold += [self.rect.centerx,self.rect.centery]
            self.new_entities.append(Bullet(self.rect.centerx-2,self.rect.centery-2, [hold[0],hold[1]] ))
            self.clicked = True
        elif not mouse_press[0]:
            self.clicked = False
    


class Wall_Manager():
    def __init__(self, enitity_list):
        self.walls = list() #a list of list(class Wall) it keeps tracks of all the walls

        for entity in enitity_list:
            if type(entity) is Wall:
                self.walls.append(entity)

        self.orient_walls()

        self.load_wall_textures()
        
    def load_wall_textures(self):
        for wall in self.walls:
            wall.get_texture_from_orientation()
            wall.load_textures()

    def extend_wall(self, origin_wall, wall_block, orientation):
        """
            adds wall_block onto the end of origin_wall

            Parameters
            ----------

            origin_wall:
                list() type = class Wall

            wall_block:
                class Wall

            orientation:
                str() of choice(["up", "down" , "left", "right"])

            Returns
            -------
            the extended wall

        """
        last_block = origin_wall[-1]
        if orientation == "up":
            pass
        elif orientation == "down":
            pass
        elif orientation == "left":
            pass
        elif orientation == "right":
            pass

    def orient_walls(self):
        for wall in self.walls:
            self.orient_wall(wall)

    def orient_wall(self, wall):
        wall.connected_sides = list()
        for test_wall in self.walls:
            flushed_sides = self.get_flushed_axis(wall, test_wall)
            if len(flushed_sides) == 1:

                wall.connected_sides.extend(flushed_sides)
                wall.connected_walls.append(wall)



    def get_flushed_axis(self, reference_wall, test_wall):
        touch_sides = list()
        if reference_wall.rect.bottom == test_wall.rect.top:
            touch_sides.append("bottom")

        if reference_wall.rect.top == test_wall.rect.bottom:
            touch_sides.append("top")

        if reference_wall.rect.left == test_wall.rect.right:
            touch_sides.append("left")

        if reference_wall.rect.right == test_wall.rect.left:
            touch_sides.append("right")

        # if "left" in touch_sides and "right" in touch_sides:
        #     if "top" in touch_sides:
        #         return "top"
        #     elif "bottom" in touch_sides:
        #         return "bottom"

        # elif "top" in touch_sides and "bottom" in touch_sides:
        #     if "left" in touch_sides:
        #         return "left"
        #     elif "right" in touch_sides:
        #         return "right"
        return touch_sides  

class Wall(Entity):
    def __init__(self, x=0, y=0,w=64,h=64):
        super().__init__(x,y,w,h,load_texture = False)
        self.connected_sides = list()
        self.connected_walls = list()

    def get_texture_from_orientation(self):
        for entry in os.scandir("textures/Walls"):
            if entry.is_dir():
                file_hints = entry.path.split("_") 
                if len(self.connected_sides) == 1 and self.connected_sides[0] in file_hints and not "corner" in file_hints:
                    self.texture_loc = entry.path
                elif len(self.connected_sides) == 2 and all( [side in file_hints for side in self.connected_sides]):
                    self.texture_loc = entry.path
                else:
                    pass

                # if :
                #     if "corner" in entry.path.split("_"):
                #         if len(self.connected_sides) > 1:
                            

                #     else:
                #        self.texture_loc = entry.path 
        print(self.connected_sides)
        print(self.texture_loc)


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
        # a float location is needed for good moving along an angle.
        self.actual_fucking_location = [x,y]
        #the location it is going to
        self.goal_position = goal_position
        #initial direction, stops going here after a ricochet
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


        
        #try to move in a direction, gather boxes it collides with
        self.rect.move_ip(self.speed_x, 0)
        self.actual_fucking_location[0] += self.speed_x
        boxes = []
        ents = []
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Type:
                boxes.append(k.rect)
                ents.append(k)

        
        # if collision then adjust coords and ricochet
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
        

        #same as above but in the y direction
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

class Energy(Entity):
    def __init__(self, x,y):
        super().__init__(x,y,8,8,texture_loc= "textures/Battery")
        self.energyBoost = 2500
    def update(self,_,__,___,entities):
        boxes = []
        ents = []
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Player:
                boxes.append(k.rect)
                ents.append(k)
        # if collision then adjust coords and ricochet
        rcti = self.rect.collidelist(boxes)
        if rcti != -1:
            ent = ents[rcti]
            ent.energy += self.energyBoost
            del entities[entities.index(self)]

        
class Enemy(Entity):
    def __init__(self, x,y):
        super().__init__(x,y,32,32,texture_loc= "./textures/Enemy")
    def update(self,_,__,___,entities):
        boxes = []
        ents = []
        for k in entities:
            if self.rect.colliderect(k.rect) and k != self and type(k) == Bullet:
                boxes.append(k.rect)
                ents.append(k)
        # if collision then adjust coords and ricochet
        rcti = self.rect.collidelist(boxes)
        if rcti != -1:
            del entities[entities.index(self)]