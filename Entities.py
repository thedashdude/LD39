#import basic pygame modules
import pygame
from pygame.locals import *

class Entity():
	def __init__(self,current_world, x=0, y=0, length = 32, width = 32):
		self.x = 0
		self.y = 0
		self.current_world = current_world
		self.rect = Rect(self.x,self.y,length,width)

		self.new_entities = None

	def move(self,x,y):
		self.x += x
		self.y += y
		

	def update(self, keystate, mouse_position, mouse_press, collided_entites):
		pass

	def get_new_entities(self):
		x = self.new_entities
		self.new_entities = None
		return x

	def get_collision_box(self):
		return self.rect

	def draw(self, screen):
		pass

